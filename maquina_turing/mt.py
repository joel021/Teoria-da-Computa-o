class MT(): #Turing Machine

    def __init__(self):
        pass

    def auto_run(self):
        
        E = input().split(" ") #1° line: list of states
        alphabet = input().split(" ") #2° line: alphabet
        tape_alphabet = input().split(" ") #3° line: the alphabet of the data tape
        self.l_limiter = input() #4° line: data tape left limiter
        self.white = input() #5° line: the white character
        n = int(input()) #n transactions

        #----- set states ------
        alphabet.append("*") #make sure the alphabet have the empty character
        
        #initialize the data tape
        tape_alphabet = [self.l_limiter] + tape_alphabet #add left limiter
        tape_alphabet.append(self.white) #make sure the data tape have white character after left limiter

        iteractions = []
        for i in range(n):
            iteractions.append(input())

        self.mt_graph = self._build_graph(E, alphabet, tape_alphabet, iteractions)

        self.init_state = str(input())

        self.final_states = str(input()).split(" ")

        words = input().split(" ")

        for word in words:
            print(self.extended_delta(list(word)))

    def _build_graph(self, E, alphabet, tape_alphabet, iteractions):
        """Initialize the graph which describes the rule of transactions.

        @E: (List) list of states
        @alphabet: (List) the set of characters of alphabet (Σ)
        @tape_alphabet: (List) the set of characters of alphabet (Γ)
        Σ is subset of Γ
        """
        mt_graph = dict()

        for e in E: #initialize the graph
            for c in alphabet: 
                mt_graph[(e, c)] = []
                mt_graph[(e, c)] = []
                mt_graph[(e, c)] = []

            for c in tape_alphabet: 
                mt_graph[(e, c)] = []
                mt_graph[(e, c)] = []
                mt_graph[(e, c)] = []

        for it in iteractions: #to each n iteration, receive <a, b, c, d, e>:
            """
            a: 0 = start state, b: 1 = character on tape, c: 2 = destination state, 
            d: 3 = character to be writed on tape, e: 4 = direction (E = left, D = right, I = feft before right)
            """
            s = it.split(" ")
            mt_graph[(s[0], s[1])].append((s[2], s[3], s[4])) #(a, b)_<p> -> [(c, d, e)_1, (c, d, e)_2, ..., (c, d, e)_n]

        return mt_graph

    def direction(self, d, i):
        
        if d == "D":
            return i + 1
        
        if d == "E":
            return i - 1

        return i

    def extended_delta(self, tape):

        if not self.l_limiter in tape: #Make sure the tape is with correct shape
            tape = [self.l_limiter] + tape
        tape.extend( list(self.white*10)) #10 is margin to avoid index out range.

        threads = [(self.init_state, 1, tape)] # (current state, heah position, tape data)
        
        while threads:
            c_ste, i, tape_t = threads.pop() #tape_t: tape at thread t. Each thread have a tape
            
            transactions = self.mt_graph[(c_ste, tape_t[i])]  #Transactions we have to state c_ste receiving word_i
            
            if c_ste in self.final_states and len(transactions) == 0: #if current state is a final state and new transactions to this thread doesn't exists
                return "S" #is accepted

            self.delta(i, transactions, tape_t, threads)
            
        return "N"

    def delta(self, i, transactions, tape_t, threads):
        """Process transactions. Return (bool).
        Return True only if the current thread stop on final state and have not new transactions to do
        @i: (int) head position
        @transactions: (List) transactions to current thread
        @tape_t: (List) data tape to current thread
        @threads: (List) remain threads to be processed
        """
        for c, d, e in transactions: #c: new state, d: character to be writed on tape_t[i], e: direction
            i_ = self.direction(e,i) #change the head position based on direction definition
            tape_t_ = tape_t.copy() #make sure not change the current tape_t to avoid conflits
            tape_t_[i] = d #write the character e at i position of new tape_t
            threads.append((c, i_, tape_t_)) #insert on threads to be processed

    def setup(self, definition):
        """Method to test the algorithm
        @Definition: (Dataframe)
        """
        E = definition[0].split(" ") #1° line: list of states
        alphabet = definition[1].split(" ") #2° line: alphabet
        tape_alphabet = definition[2].split(" ") #3° line: the alphabet of the data tape
        self.l_limiter = definition[3] #4° line: data tape left limiter
        self.white = definition[4] #5° line: the white character
        n = int(definition[5]) #n transactions

        #----- set states ------
        alphabet.append("*") #make sure the alphabet have the empty character
        
        #initialize the data tape
        tape_alphabet = [self.l_limiter] + tape_alphabet #add left limiter
        tape_alphabet.append(self.white) #make sure the data tape have white character after left limiter

        iteractions = []
        for i in range(6, n+6, 1):
            iteractions.append(definition[i])

        self.mt_graph = self._build_graph(E, alphabet, tape_alphabet, iteractions)

        self.init_state = str(definition[n+6])

        self.final_states = str(definition[n+7]).split(" ")

if __name__ == "__main__":
    turing_machine = MT()
    turing_machine.auto_run()