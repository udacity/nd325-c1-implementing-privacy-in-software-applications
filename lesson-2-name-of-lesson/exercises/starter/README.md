# Lesson 2: Exercise 2 - Deletion

In this exercise, we've provided you with some starter code in the `main` directory.
The goal here is to implement deletion for a store that contains candidates for hiring.

The only file you should need to modify is the `src/main/hiring_store.py` file. This is a file
that manages an ephemeral SQLite database. This file is used by the `src/main/api.py` file for
our API layer (shouldn't need to modify this), and the `src/test/test_hiring_store.py` file is
where our tests live.

Implement the `soft_delete_candidate` method, and the `hard_delete_candidate` methods.
This method should soft delete and hard delete the `Candiate` from the store.

If done correctly, in the `src/test/test_hiring_store.py`, the `test_hard_delete` and `test_soft_delete` methods should
pass. The only test that should not pass is `test_data_subject_access_request`.

To run tests, run `pytest` from the `src/` directory.

# Lesson 2: Exercise 3 - Data Subject Access Request

In this exercise, we've provided you with some starter code in the `main` directory.
The goal here is to implement a Data Subject Access Request method that respects soft deletion.

Implement the `soft_delete_candidate` method, and the `hard_delete_candidate` methods.
This method should soft delete and hard delete the `Candiate` from the store.

If done correctly, in the `src/test/test_hiring_store.py`, the `test_data_subject_access_request` should pass.

To run tests, run `pytest` from the `src/` directory.
