#comment/Uncomment these lines to import the libraries once you have installed them:

from binarytree import Node
import matplotlib.pyplot as plt
from datetime import datetime

#Visualize Data
def display_growth(sd):
    date = [[datetime.strptime(sd[country][day][0], '%Y-%m-%d') for day in range(len(sd[country]))] for country in sd]
    
    count = [[sd[country][day][1] for day in range(len(sd[country]))] for country in sd]
    
    country = [country for country in sd]
    
    palette = plt.get_cmap('hsv',len(sd))
    fig = plt.figure(num=None, figsize=(20, 10), dpi=80, facecolor='w', edgecolor='k')
    for i in range(len(sd)):
        date[i], count[i] = (list(t) for t in zip(*sorted(zip(date[i], count[i]))))
        plt.plot(count[i], 'o-', color=palette(i+1), linewidth=1, alpha = 0.9, label = country[i])
        
    plt.legend(loc="upper left")
    plt.title("COVID-19 Cases in Selected Countries",fontdict = {'fontsize' : 20})
    plt.xlabel("Date", fontdict = {'fontsize' : 15})
    xticks = [i.strftime('%Y-%m-%d') for i in date[0]]
    plt.xticks(range(len(xticks))[1::2], xticks[1::2])
    fig.autofmt_xdate()
    plt.ylabel('Number of Cases',fontdict = {'fontsize' : 15})
    plt.show()

#Print BInary Tree Information
def Print_tree(node, date, level, direction):  
    
    print("Tree Level:", level,',', "Number of Countries in Node:", len(node.countries),',', direction)
    print("split_number:", node.split_number)
    
    for i in node.countries:
        country_out = "(" + i.country_name + "," + str(i.day_count(date)) + ")"
        print(country_out + ",", end =" ")
    print("\n")
        
    if node.left:  
        Print_tree(node.left, date, level+1, "Left Child")
            
    if node.right:
        Print_tree(node.right, date, level+1, "Right Child")  

#Build the binary tree of split_numbers
def buildbtree_node(node):
    root = Node(int(node.split_number))

    if node.left:
        root.left = buildbtree_node(node.left)

            
    if node.right:
        root.right = buildbtree_node(node.right)
        
    return root

print_details = True

#Use this method to visualize the binary tree and information
def display_tree(tree_root, date):
    """
    This method will visualize the tree
    """
    my_tree = buildbtree_node(tree_root)
    print("Binary Tree showing split_number:")
    print(my_tree)
    
    if print_details: 
    	print("Detailed information about your binary tree: \n")
    	Print_tree(tree_root, date, 0, "Root")
    
