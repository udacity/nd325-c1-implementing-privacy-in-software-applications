## Prep

1. Open up `user_store.py` in Pycharm
2. `cd ~/Projects/Udacity Privacy Engineering/nd325-c1-implementing-privacy-in-software-applications/lesson-2-name-of-lesson/demos`


## Script
In this demo, I'll be showing you how to soft delete data and hard delete data, as well as how to perform a data subject
access request in a very simple system.

We're going to be using Python for this, but if you're familiar with SQL, you'll
notice some SQL commands in the code.

#### GO TO `user_store.py`
Here, we have just simple a one-file program. It's just a user store for any arbitrary application.

#### Point to `User` class
Up top here we have a simple User class, that has the name of the user, their email address and their user ID

#### Point to `UserStore.create_tables` method
And here we have our simple user store. You'll see that this is where we create our `users` table. If we wanted to create
more tables, we could add them and their schemas here.

#### Scroll down to the implemented methods
Now, if we scroll down, we'll see we have an add user and get user methods already built out.
We'll use these methods for testing later.

#### Scroll further down to the unimplemented methods
These are the three methods we want to implement here. There's soft delete, hard delete, and the subject access request.
Let's first start with soft delete. To do this, we're going to have to first add in some sort of marker to indicate that
something has been soft deleted. In this case, what I'm going to do is add an extra column to this table to make that
clear.

#### Go to the `create_tables` method and add in an integer `soft_delete` column.
I'm using the value as an integer here because this is a very basic version of SQL, but really it could just be a
boolean if that's available to you in your database. After we do this, we have to modify the existing methods to work
with this new column.

#### Modify the `add_user` method for soft deletion
Here, we add in the `soft_deleted` value to be `0`.

#### Modify the `get_user` method for soft deletion
```
if not user_row or user_row[3] == 1:
    return None
```
Then for getting the user, we have to return `None` if the user is soft deleted,
because soft delete means that this data is inaccessible, even though it might still be present.

#### Write soft deletion
Perfect. Now we have to actually write soft deletion. All we have to do is set the value of the soft deletion column to
one. Let's do that real fast.

```
def soft_delete_user(self, user_id: int):
    self.connection.execute("""UPDATE users SET soft_deleted=1 WHERE user_id=?""", (user_id,))
    self.connection.commit()
```
Here's a simple SQL command that sets the `soft_deleted` cell to one for the given user ID.

#### Test Soft Delete
Cool! Let's give it ago in the terminal!
```
>>> python3 -i user_store.py
>>> user_store = UserStore.get_instance()
>>> user_store.add_user("Linda Chi", "lchi@email.com")
1
>>> user_store.get_user(_).full_name
'Linda Chi'
>>> user_store.soft_delete_user(1)
>>> user_store.get_user(1)
None
```

#### Try Hard Delete
Cool! Now that we've taken care of soft deletion, let's give hard deletion a try. All we have to do here, actually
delete the row from the table.
```
def hard_delete_user(user_id: int):
    self.connection.execute("""DELETE FROM users WHERE user_id=?""", (user_id,))
    self.connection.commit()
```
So again, we're writing a simple SQL command to do the deletion for us, and then committing.

#### Try Data Subject Access Request
Now, we should test hard deletion, but we really can't because we have no way to distinguish between hard and soft
deletion in this code; no matter which type of deletion we use, if we call our `get_user` method, we won't get it back.

However, during a data subject access request, we must return the data corresponding to user, even if that data has been
soft deleted. This is because that data still lives and is managed by your system. However, in the case of hard delete,
your system no longer manages or has control of that data, so there is no way for you to return it.

Let's give a Data Subject Access request a shot here.

```
def user_data_subject_access_request(self, user_id: int) -> Optional[User]:
    cursor = self.connection.cursor()
    cursor.execute("""SELECT * FROM users WHERE user_id=?""", (user_id,))
    user_row = cursor.fetchone()
    self.connection.commit()

    if not user_row:
        return None

    return jsons.dumps(Candidate(user_id, user_row[1], user_row[2]))
```

So this is just like the `get_user` method above, except now, instead we don't pay heed to the `soft_deleted` column, as
we must return everything that lies in this table. Let's give this a quick test.


#### Switch to Terminal
```
>>> python3 -i user_store.py
>>> user_store = UserStore.get_instance()
>>> user_store.add_user("Linda Chi", "lchi@email.com")
1
>>> user_store.get_user(_).full_name
'Linda Chi'
>>> user_store.soft_delete_user(1)
>>> user_store.get_user(1)
None
>>> user_store.data_subject_access_request(1).full_name
'Linda Chi'
>>> user_store.hard_delete_user(1)
>>> user_store.data_subject_access_request(1).full_name
None
```
