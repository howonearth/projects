# CS50 Python Final Project
# SHOPPING LIST MANAGER
#### Video Demo:  https://youtu.be/uwbHsf9QVUE
#### Description:

Most of us go shopping to the same places and we tend to buy the same things there, especially when it comes to grocery shopping, but it’s not limited to it... Wouldn’t it be nice to store all your typical shopping lists for each store in the same application? Let me present the shopping list manager that I’ve created.

The main menu lets you choose one of five actions. The application restores this menu after each operation until you precisely tell it to exit.

The very first thing you can do is create a shopping list by inputing “1” and then adding the name of the store. The program then adds the name of the store to the table in the database and automatically assigns it an id.

After that you can add a typical list of products that you buy from that store(input "2"). You should choose one of the stores that you’ve already added and then type the items, press Enter after each of them and press Ctrl-D when you’re done. The program then stores all the products in another table in the database together with the id of the shop that you selected.

By choosing the action number 3 in the main menu you can consult the lists that you’ve already created. The program outputs the list of shops you go to and you are required to select a corresponding number. After you select the shop, you will see the list of products that you’ve assigned to this store. You can add more products later, the lists are not final.

You can also delete a whole shopping list if you, say, moved or you decided to boycott the store for some reason and you don’t go there anymore. Deleting a whole shopping list is a big decision and you don’t want to do that accidentally so the program asks you to confirm that you really do want to delete it. If you type something other than “yes”, you will receive a notification saying “Action aborted!” After you confirm the action, the program deletes the name of the store from the database and all the products assigned to this store's id in the database, the shopping list will be deleted permanently and not restorable.

You can also delete some items from a particular list. For this you first select the store and the program automatically shows you the shopping list for this store, for reference. Then you are prompted to list the items that you want to delete. Deleting the products follows the same principle as adding them to the list: you press Enter after each item and Ctrl-D when you are done. After you press Ctrl-D, the program checks if all the items were on the list you selected, and gives you a summary of the action. It then deletes the items that were on the list from the database and ignores the ones that were not on the list. When you receive the notification about the items that were not on the list you can probably notice that they either were not on the list or you misspelled them. That is when having the program return you the list for the particular store before you list the items you want to delete comes in handy. You can consult the list and then pay attention to, say, plurals or misspellings in the existing list and input the items accordingly.

When you exit the program by inputting 5 after the main menu, the application is being very polite and wishes you happy shopping.
