from RedBlackBST import RedBlackBST as BST
example='SEARCHEXAMPLE'
values=list(range(0,13))
bst=BST()
print('Building Red-Black Tree...')
for key,value in zip(example,values):
    bst.put(key,value)
print('Printing Red Black Tree...')
bst.llrbprint()
print('Properties of This Red-Black Tree:')
print('Size:', bst.size())
print('Min:',bst.min())
print('Max:',bst.max())
print('Rank of E:',bst.rank('E'))
print('Floor of G:',bst.floor('G'))
print('Select Index 1:',bst.select(1))
print('Deleting M ...')
bst.delete('M')
print('Current Size:', bst.size())
print('Deleting What\'s Left')
while bst.size()>0:
    print('Deleting',bst.min(),'...')
    bst.deleteMin()
    print('Current Size:',bst.size())
