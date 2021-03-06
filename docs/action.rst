.. DOBOTO documentation sub class file, created bysphinxter.py.

Action (do.action)
============================================

Actions are records of events that have occurred on the resources in your account. These can be things like rebooting a Droplet, or transferring an image to a new region.

An action dict is created every time one of these actions is initiated. The action dict contains information about the current status of the action, start and complete timestamps, and the associated resource type and ID.

Every action that creates an action dict is available through this endpoint. Completed actions are not removed from this list and are always available for querying.

Data Structures
-----------------------

Action
^^^^^^^^^^^^^^^^^^^^^^^^^

- *id* - number - A unique numeric ID that can be used to identify and reference an action.

- *status* - string - The current status of the action. This can be "in-progress", "completed", or "errored".

- *type* - string - This is the type of action that the dict represents. For example, this could be "transfer" to represent the state of an image transfer action.

- *started_at* - string - A time value given in ISO8601 combined date and time format that represents when the action was initiated.

- *completed_at* - string - A time value given in ISO8601 combined date and time format that represents when the action was completed.

- *resource_id* - number - A unique identifier for the resource that the action is associated with.

- *resource_type* - string - The type of resource that the action is associated with.

- *region* - nullable string - (deprecated) A slug representing the region where the action occurred.

- *region_slug* - nullable string - A slug representing the region where the action occurred.



List all Actions
----------------------------------------------------------------------------------------------------

.. method:: do.action.list()


Returns:

- A list of Action data structures



Related:

* `<https://developers.digitalocean.com/documentation/v2/#list-all-actions>`_



Retrieve an existing Action
----------------------------------------------------------------------------------------------------

.. method:: do.action.info(id)

- *id* - number - The id of the Action requested


Returns:

- An Action data structure



Related:

* `<https://developers.digitalocean.com/documentation/v2/#retrieve-an-existing-action>`_

