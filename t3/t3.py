class AFNDP():

    def auto_run(self ):
        self.afd_graph = dict()
        E = input().split(" ") #list of states
        alphabet = input().split(" ") #alphabet
        alphabet_stack = input().split(" ")

        #----- set states ------
        alphabet.append("*")
        alphabet_stack.append("*")
        for e in E:
            for c in alphabet:
                for a_s in alphabet_stack:
                    self.afd_graph[(e, c, a_s)] = []

        n = int(input()) #n transactions

        for i in range(n):
            s = input().split(" ")
            self.afd_graph[(s[0], s[1], s[2])].append((s[3], list(s[4])))

        self.init_state = str(input())

        self.final_states = str(input()).split(" ")

        words = input().split(" ")

        for word in words:
            print(self.extended_delta(word))

    def extended_delta(self, word):
        
        states_stack = [(self.init_state, word, ["*"])] # (current state, remaining chars, stack)
        
        while states_stack:
            c_ste, word_i, stack = states_stack.pop()
            stack = self.clear_lambda(stack)

            #what transactions we have to state c_ste receiving word_i and unstacking stack.pop() elements:
            new_states = self.afd_graph.get((c_ste, word_i[0], stack[-1]), [])  #get a state and the word to be stacked
            if self.delta(word_i, new_states, stack[0:-1], states_stack):
                return "S"

            new_states = self.afd_graph.get((c_ste, word_i[0], "*"), []) #Seach for transaction consuming a char and not unstacking
            if self.delta(word_i, new_states, stack, states_stack):
                return "S"

            new_states = self.afd_graph.get((c_ste, "*", stack[-1]), []) #Seach for transaction without consuming a char and unstacking
            if self.delta("*"+word_i, new_states, stack[0:-1], states_stack):
                return "S"
                
            new_states = self.afd_graph.get((c_ste, "*", "*"), []) #without consuming char and without unstacking
            if self.delta("*"+word_i, new_states, stack, states_stack):
                return "S"
        
        return "N"
        
    def is_empty(self, l):
        for e in l:
            if e != "*":
                return False

        return True

    def clear_lambda(self, l):
        new_l = ["*"]
        for e in l:
            if e != "*":
                new_l.append(e)
        return new_l

    def delta(self, word_i, new_states, stack, states_stack):
        
        for new_e, word_stack in new_states:
            
            if not self.is_empty(word_stack): 
                word_stack = stack + word_stack #insert the new word of the new e on the stack
            else:
                word_stack = stack

            if new_e in self.final_states and not word_i[1:].replace("*", "") and self.is_empty(word_stack):
                return True #is accepted

            r_word = word_i[1:]
            if not word_i[1:]:
                r_word = "*"

            states_stack.append((new_e, r_word, word_stack))

        return False

    def setup(self, definition):
        self.afd_graph = dict()
        E = definition["E"].split(" ") #list of states
        alphabet = definition["alphabet"].split(" ") #alphabet
        alphabet_stack = definition["alphabet_stack"].split(" ")

        #----- set states ------
        alphabet.append("*")
        alphabet_stack.append("*")
        for e in E:
            for c in alphabet:
                for a_s in alphabet_stack:
                    self.afd_graph[(e, c, a_s)] = []

        #n = int(definition["n"]) #n transactions

        for t in definition["afd_graph"].split(";"):
            s = t.split(" ")
            self.afd_graph[(s[0], s[1], s[2])].append((s[3], list(s[4])))

        self.init_state = definition["init_state"]
        self.final_states = definition["final_states"].split(" ")


#afndp = AFNDP()
#afndp.auto_run()

with open("words.txt", "w") as f:
    f.write("mada")