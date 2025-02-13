#!/usr/bin/env python
# coding: utf-8



# -------------------------------
# Import modules
import csv
from math import pow
import numpy as np
import sys
import os
# -------------------------------


class Position:
    """
    Class describing a bidimensional position in space, which is described by x and y coordinates.
    """
    def __init__(self,x,y):
        self.x = float(x)
        self.y = float(y)
    def distanceTo(self,other):
        return np.sqrt(pow((self.x-other.x),2) + pow((self.y-other.y),2))

class Locus:
    """
    Class describing the locus of a sequence.
    A locus is defined by the chromosome number and the chromosome arm.
    A locus can be lexographically compared to other ones based on chr number and arm.
    """
    def __init__(self,name):
        pos_arms = ["p","q"]
        for arm in pos_arms:
            if arm in name:
                splitted_name = name.split(arm)
                self.chrom = name.split(arm)[0]
                self.arm = arm
    def __ge__(self,other):
        if int(self.chrom) > int(other.chrom):
            return True
        elif  not (int(self.chrom) != int(other.chrom) or self.arm < other.arm):
            return True
        else:
            return False
    def __gt__(self,other):
        if int(self.chrom) > int(other.chrom):
            return True
        elif  int(self.chrom) == int(other.chrom) and self.arm > other.arm:
            return True
        else:
            return False
    def __le__(self,other):
        if int(self.chrom) < int(other.chrom):
            return True

        elif not (int(self.chrom) != int(other.chrom) or self.arm > other.arm):
            return True
        else:
            return False

    def __eq__(self,other):
        if  int(self.chrom) != int(other.chrom) or self.arm != other.arm:
            return False
        else:
            return True



class Node:
    """
    General node class for a double-linked list.
    """
    def __init__(self,id,nextNode = None,prevNode = None):
        self.id = id
        self.next = nextNode
        self.prev = prevNode
    def print_it(self):
         print(str(self.id))
    def hasNext(self):
        if self.next == None:
            return False
        elif self.next.id == None:
            return False
        else:
            return True
    def hasPrev(self):
        if self.prev == None:
            return False
        else:
            return True




class SequenceNode(Node):
    """
    Inherited by Node class. It is a Node having as well locus and position information.
    """
    def __init__(self,id,locus,position,nextNode = None):
        self.id = id
        self.locus = locus
        self.position = position
        self.next = nextNode

    def getArm(self):
        return(str(self.locus.chrom)+str(self.locus.arm))

    def distanceTo(self,other):
        return self.position.distanceTo(other.position)

    def print_it(self):
        print(str(self.id)+", "+str(self.locus.chrom)+""+str(self.locus.arm)+", ("+str(self.position.x)+", "+str(self.position.y)+")")

    def hasSameArm(self,other):
        if self == None or other == None:
            return False
        elif self.locus == other.locus:
            return True
        else:
            return False
    def __ge__(self,other):
        if self.locus >= other.locus:
            return True
        else:
            return False
    def __le__(self,other):
        if self.locus <= other.locus:
            return True
        else:
            return False
    def __gt__(self,other):
        if self.locus > other.locus:
            return True
        else:
            return False
class DistanceNode(Node):
    """
    Inherited by Node class. It is a Node having as id the locus and n as a count.
    """
    def __init__(self,id,n,nextNode = None,prevNode = None):
        self.id = id
        self.n = n
        self.next = nextNode
        self.prev = prevNode
    def print_it(self):
        print(str(self.id)+", "+str(self.n) )



class LinkedList:
    """
    Implementation of a single linked list
    """
    global root
    global before_last
    global last

    def __init__(self,root = None, before_last = None ):
        self.root = root
        self.before_last = before_last

    # Traverse the linked-list and prints out the content
    def traverse(self):
        node = self.root
        while node != None:
            node.print_it()
            node = node.next

    # Push a node at the beginning of the list
    def push(self, node):
        if self.root == None:
            self.root = node
        if self.before_last == None:
            self.before_last = node
        else:
            node.next = self.root
            self.root = node
    def append(self,node):
        if self.root == None:
            self.root = node
        if self.before_last == None:
            self.before_last = node
        else:
            if self.before_last.next == None:
                last = self.before_last
            else:
                last = self.before_last.next
            last.next = node
            self.before_last = last
    # Gets a node in a determined position
    def get(self,position):
        i = 0
        node = self.root
        while i != position:
            node = node.next
            i+=1
        return node

    def insertAfter(self,node,current):
        if  current == self.before_last:
            self.before_last = node
        elif current == self.before_last.next:
            self.before_last = self.before_last.next
        node.next = current.next
        current.next = node



def insert_node(sl,node):
    """
    Inserts a node in a sorted linked list in the rigth position.
    """
    if sl.root == None:
        sl.root = node
    if sl.before_last == None:
        sl.before_last = node
    else:
        # put at the beginning
        if sl.root >= node:
            temp = sl.root
            sl.root  = SequenceNode(node.id,node.locus,node.position,temp)
        elif not ( sl.before_last.next == None or sl.before_last.next  > node):
            #print("end case")
            sl.append(node)
        else:
            #print("middle /end case")
            current = sl.root
            current_prev = sl.root
            while current != None and current < node:
                current_prev = current
                current = current.next
            sl.insertAfter(node,current_prev)



# In[299]:


def create_sequence_linkedList(infile):
    """
    Creates a linked list of nodes based on the input files.
    Returns the sorted linked list.
    """
    ll = LinkedList()
    with open(infile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            # Create a Node Instance for each line read
            x = row[2].split(',')[0].replace("(","")
            y = row[2].split(',')[1].replace(")","")
            node = SequenceNode(row[0],Locus(row[1]),Position(x,y))
            insert_node(ll,node)

    return(ll)




def print_out(ll,outfile):
    """
    Prints the content of the linked list in a tab-separated file.
    """
    file = open(outfile,"w")
    node = ll.root
    while node != None:
        file.write(str(node.id)+"\t" + str(node.n) + "\n")
        node = node.next




def calc_distances(ll,k):
    """
    Calculates the distance
    """
    distance_list = LinkedList()
    left_node = ll.root
    count  = 0
    while left_node != None:
        current_node = left_node.next
        if(left_node.hasSameArm(current_node)):
            samechromarm=True
        else:
            # Changes the Chromosome arm!
            # We need to save current stuff and rebegin the count
            distance_list.append(DistanceNode(left_node.getArm(),count))
            count = 0
            left_node = left_node.next
            continue
        while current_node != None and samechromarm :
            if not left_node.hasSameArm(current_node):
                samechromarm=False
                continue
            if(left_node.distanceTo(current_node)<=k):
                count += 1
            current_node = current_node.next
        left_node = left_node.next
    return(distance_list)



if __name__ == "__main__":
    # Collects command line inputs
    infile = sys.argv[1]
    k = float(sys.argv[2])
    # Creates and sort the Linked List based on the input file
    sequence_ll = create_sequence_linkedList(infile)
    dist_ll = calc_distances(sequence_ll, k)

    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    outfile = os.path.join("outputs","output_"+os.path.basename(infile))
    print_out(dist_ll,outfile)
    print("\n")
    print("Done!\n")
    print("The output can be found at :")
    print(outfile+"\n")


# infile ="/Users/luisasantus/Desktop/apa/Assignment2/inputs/input1.txt"
# sequence_ll = create_sequence_linkedList(infile)
# sequence_ll.traverse()
# dist_ll = calc_distances(sequence_ll, 1.5)
# dist_ll.traverse()


# In[ ]:





# In[ ]:
