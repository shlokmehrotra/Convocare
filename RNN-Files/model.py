# Torch imports
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

# General imports
import numpy as np
from collections import Counter


# Importing s2t function from v2 // can diff. speakers
from speech2text-v2 import speech2text

# Processing wav file
raw_script = speech2text("doctor.wav")

# Preprocessing given data
def preprocess(raw_script):
    """
    Processes the script, labels doctor and patient script.
    ________________________________
    Args: raw_script data
    Returns: - set of vocabulary with all words in the conversation.
               (for word embeddings that will be passed into the LSTM network.)
             - list of entire conversation batched for training.

    """

    # Indices that API generates, inconsistent; hence, cleaned here.
    speaker_idxs = set([sublist[1] for sublist in raw_script])
    # Character vocabulary array
    vocabulary = [sublist[0] for sublist in raw_script]

    # Doctor is first to speak
    doctor = raw_script[0][1]

    # Changes speaker indices to doctor or patient for training purposes.
    for sublist in raw_script:
        if sublist[1] == doctor:
            sublist[1] = "doctor"
        else:
            sublist[1] = "patient"

    return vocabulary, raw_script


# token replacement, punctuation to char.
def token_lookup():
    """
    Generate a dict to turn punctuation into a token.
    ________________________________
    Returns: Tokenize dictionary where the key is the punctuation and the value is the token
    """
    return {
        '.': '||PERIOD||',
        ',': '||COMA||',
        '"': '||QUORATION_MARK||',
        ';': '||SEMICOLON||',
        '!': '||EXCLAMATION_MARK||',
        '?': '||QUESTION_MARK||',
        '(': '||LEFT_PARENTHESIS||',
        ')': '||RIGHT_PARENTHESIS||',
        '--':'||DASH||',
        '\n':'||NEW_LINE||'
    }


# word2int and int2word mapping
def mapping(vocabulary):
    """
    Returns two hash tables including word2int and int2word mappings using
    counter from collections library.
    ________________________________
    Args: vocabulary
    Returns: - 2 hash tables to look convert words to corresponding ints.

    """

    # set to get rid of repition
    word_counts = Counter(vocabulary)
    sorted_vocab = sorted(word_counts, key=word_counts.get, reverse=True)

    # dict comprehension to generate hash tables
    int2vocab = {ii: word for ii, word in enumerate(sorted_vocab)}
    vocab2int = {word: ii for ii, word in int_to_vocab.items()}

    # return tuple
    return (vocab_to_int, int_to_vocab)


# LSTM class
class RecurrentLSTM_Net(nn.Module):
    # initialization function
     def __init__(self, vocab_size, output_size, embedding_dim, hidden_dim, n_layers, dropout=0.5):
        """
        Initialize the PyTorch RNN Module
        ________________________________
        Args:
            - The number of input dimensions of the neural network (the size of the vocabulary)
            - The number of output dimensions of the neural network
            - The size of embeddings, should you choose to use them
            - The size of the hidden layer outputs
            - dropout to add in between LSTM/GRU layers

        Methods:
            - forward
            - init_hidden
        """
        super(RNN, self).__init__()

        # set class variables
        self.output_size = output_size
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers

        # define model layers
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, n_layers, batch_first=True, dropout=dropout)

        self.fc = nn.Linear(hidden_dim, output_size)

    # forward pass
    def forward(self, nn_input, hidden):
        """
        Forward propagation of the neural network
        ________________________________
        Args: - The input to the neural network
              - The hidden state
        Returns: Two Tensors, the output of the neural network and the latest hidden state
        """
        batch_size = nn_input.size(0)

        embeds = self.embedding(nn_input)
        lstm_out, hidden = self.lstm(embeds, hidden)

        lstm_out = lstm_out.contiguous().view(-1, self.hidden_dim)

        out = self.fc(lstm_out)

        out = out.view(batch_size, -1, self.output_size)
        out = out[:, -1]

        # return one batch of output word scores and the hidden state
        return out, hidden

    # initialization hidden layers
    def init_hidden(self, batch_size):
        '''
        Initialize the hidden state of an LSTM/GRU
        ________________________________
        Args: The batch_size of the hidden state
        Returns: hidden state of dims (n_layers, batch_size, hidden_dim)
        '''
        # Implement function

        # initialize hidden state with zero weights, and move to GPU if available
        weight = next(self.parameters()).data

        if train_on_gpu:
            hidden = (weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().cuda(),
                     weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().cuda())
        else:
            hidden = (weight.new(self.n_layers, batch_size, self.hidden_dim).zero_(),
                      weight.new(self.n_layers, batch_size, self.hidden_dim).zero_())

        return hidden


# forward and backprop function
def forward_back_prop():
     """
    Forward and backward propagation on the neural network
    ________________________________
    Args:
        - The PyTorch Module that holds the neural network
        - The PyTorch optimizer for the neural network
        - The PyTorch loss function
        - A batch of input to the neural network
        - The target output for the batch of input
        - The loss and the latest hidden state Tensor

    Returns:
        - loss and hidden states
    """

    # move data to GPU, if available
    if train_on_gpu:
        rnn.cuda()

    # perform backpropagation and optimization
    hidden = tuple([each.data for each in hidden])
    rnn.zero_grad()

    if train_on_gpu:
        inputs, target = inp.cuda(), target.cuda()

    output, h = rnn(inputs, hidden)

    loss = criterion(output, target)
    loss.backward()

    nn.utils.clip_grad_norm_(rnn.parameters(), 5)
    optimizer.step()

    # return the loss over a batch and the hidden state produced by our model
    return loss.item(), hidden


def train_rnn(rnn, batch_size, optimizer, criterion, n_epochs, show_every_n_batches=100):
    """
    Training Loop
    ________________________________
    Args:
        - RNN model
        - Batch Size
        - Optimizer
        - Criterion
        - # of epochs
        - # frequency of batch displays
    """
    batch_losses = []

    rnn.train()

    print("Training for %d epoch(s)..." % n_epochs)
    for epoch_i in range(1, n_epochs + 1):

        # initialize hidden state
        hidden = rnn.init_hidden(batch_size)

        for batch_i, (inputs, labels) in enumerate(train_loader, 1):

            # make sure you iterate over completely full batches, only
            n_batches = len(train_loader.dataset)//batch_size
            if(batch_i > n_batches):
                break

            # forward, back prop
            loss, hidden = forward_back_prop(rnn, optimizer, criterion, inputs, labels, hidden)
            # record loss
            batch_losses.append(loss)

            # printing loss stats
            if batch_i % show_every_n_batches == 0:
                print('Epoch: {:>4}/{:<4}  Loss: {}\n'.format(
                    epoch_i, n_epochs, np.average(batch_losses)))
                batch_losses = []

    # returns a trained rnn
    return rnn

# Data params
# Sequence Length
sequence_length = 10  # of words in a sequence
# Batch Size
batch_size = 128

# data loader - do not change
train_loader = batch_data(int_text, sequence_length, batch_size)


# Training parameters
# Number of Epochs
num_epochs = 10
# Learning Rate
learning_rate = 0.001

# Model parameters
# Vocab size
vocab_size = len(vocab_to_int)
# Output size
output_size = len(vocab_to_int)
# Embedding Dimension
embedding_dim = 200
# Hidden Dimension
hidden_dim = 250
# Number of RNN Layers
n_layers = 2

# Show stats for every n number of batches
show_every_n_batches = 100


# create model and move to gpu if available
rnn = RNN(vocab_size, output_size, embedding_dim, hidden_dim, n_layers, dropout=0.5)
if train_on_gpu:
    rnn.cuda()

# defining loss and optimization functions for training
optimizer = torch.optim.Adam(rnn.parameters(), lr=learning_rate)
criterion = nn.CrossEntropyLoss()

# training the model
trained_rnn = train_rnn(rnn, batch_size, optimizer, criterion, num_epochs, show_every_n_batches)

# saving the trained mode
helper.save_model('./save/trained_rnn', trained_rnn)
print('Model Trained and Saved')
