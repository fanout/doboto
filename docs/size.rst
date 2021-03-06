.. DOBOTO documentation sub class file, created bysphinxter.py.

Size (do.size)
============================================

The sizes dict's represent different packages of hardware resources that can be used for Droplets. When a Droplet is created, a size must be selected so that the correct resources can be allocated.

Each size represents a plan that bundles together specific sets of resources. This includes the amount of RAM, the number of virtual CPUs, disk space, and transfer. The size dict also includes the pricing details and the regions that the size is available in.

Data Structures
-----------------------

Size
^^^^^^^^^^^^^^^^^^^^^^^^^

- *slug* - string - A human-readable string that is used to uniquely identify each size.

- *available* - boolean - This is a boolean value that represents whether new Droplets can be created with this size.

- *transfer* - number - The amount of transfer bandwidth that is available for Droplets created in this size. This only counts traffic on the public interface. The value is given in terabytes.

- *price_monthly* - number - This attribute describes the monthly cost of this Droplet size if the Droplet is kept for an entire month. The value is measured in US dollars.

- *price_hourly* - number - This describes the price of the Droplet size as measured hourly. The value is measured in US dollars.

- *memory* - number - The amount of RAM allocated to Droplets created of this size. The value is represented in megabytes.

- *vcpus* - number - The number of virtual CPUs allocated to Droplets of this size.

- *disk* - number - The amount of disk space set aside for Droplets of this size. The value is represented in gigabytes.

- *regions* - list - A list containing the region slugs where this size is available for Droplet creates.



List all Sizes
----------------------------------------------------------------------------------------------------

.. method:: do.size.list()


Returns:

- A list of Size data structures



Related:

* `<https://developers.digitalocean.com/documentation/v2/#list-all-sizes>`_

