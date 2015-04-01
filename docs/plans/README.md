# Next generation discussions and plans

## Next few months

### Data

#### Rationale

The data model is fundamental and is currently not serving our needs in the area of extensibility, flexibility, and performance. How we do the data models and interfaces (APIs) will affect most other pieces of the system (_e.g._, the sharing model affects UI, data protocols affect services, data storage affects search). 

#### Approach

Adam's and other existing data principles documents ([1][PoDKB], [2][KBS2]) will be major inputs, but we want to work as bottom-up as possible in the first stages to make sure we do not build a baroque second system. The working process is to roughly alternate between short cycles, 1-3 days, of design and prototyping.

* Start with the abstract data model, using as a base some simple known scientific objects, such as assembly and maybe annotation. Include all aspects of the data touched on in the principles document ([1][PoDKB]), including metadata, provenance, and sharing.
    - Output: a vocabulary, design documents and diagrams.
* Perform prototyping using some wire protocols. The prototypes should be in a few different technologies, so we can do a "bake-off" to determine which formats make the most sense. 
    - Output: Working code examples
* Design alternatives for storage. Prototyping and bake-off with at small scale.
    - Output: a vocabulary, design documents and diagrams. Working code examples. Performance numbers.
* Continue modeling to mock up a self-contained "service" that uses several data objects at once, and to include provenance and versioning in the prototypes. 
    - Output: a vocabulary, design documents and diagrams.
* More prototyping
    - Output: Working code examples
* Model complex data objects. Aim for insights into how to use polymorphism and generics, inheritance, and composition, within the KBase type system. Complex objects, like "genome", have many isomorphs and variations that must be dealt with.
    - Output: a vocabulary, design documents and diagrams.

Once these modeling concepts are understood, we can move towards the Frankenstein phase where we start building up a parallel data infrastructure for storage of the full data set, with all existing types getting moved over. This will also be the time to try some new database tech., such as MonetDB columnar storage and Hadoop/Hive/etc. indexing. Not all of this will happen in the first few months, but some will grow out of the prototyping.

## Next year

The new data design will begin to be implemented as a parallel (second) system, that will for this time be deployed alongside the existing data needed by all the existing components. Members of the data team, and other teams as necessary, will be pulled in to do this once the design and initial prototypes are complete and approved. 

Beyond June and for the rest of the year these other areas need to be addressed:
* Methods - A clean interface for adding new functionality to KBase
* Visualization - Similar in spirit to execution, allowing visualizations built by the community to be added as easily as they can currently be plugged into a vanilla Jupyter/IPython notebook
* Execution - Related to the previous two, providing a single asynchronous interface for methods that are able to run on local backends, batch backends, cluster backends, etc. A crucial difficulty is that the heavyweight methods might need a specific execution environment. Another is that provenance should be consistent, and the mechanism for providing it as transparent as possible to the user and as easy to maintain for KBase itself, as possible.
* Narrative UI - Rewriting much of the UI to live on top of the IPython3.0/Jupyter front-end, and refactoring the Docker container infrastructure to align better with the Jupyterhub backend.

Not all of this will be possible, even pulling effort from multiple teams, in the one year time frame. The new requirements from the science teams will be used to guide the order of execution. In general, we need to make sure we agree on clean and useful interfaces _first_ before building the full back-end implementations. This will make it much easier to change implementations later.

## Three year span

By this time, we want to have a far more robust and modular system from top to bottom. This is really the foundation we wanted at the last review, for data mining of annotations, references, etc. to gain new knowledge -- the raison d'etre of KBase, and something we should start on in this time span even if our initial approach is naive.
* Scalability of the data system. Faster data imports, exports, searches, etc. KBase could also index data sets whose raw data is stored outside KBase.

# References

1. [Principles of Data in KBase][PoDKB]
2. [KBase data storage 2nd round requirements][KBS2]

[PoDKB]: https://docs.google.com/a/lbl.gov/document/d/1YY7JwAdQY2bLWZl-VtTPV_K9erA8Vkak5NdXOVUQavQ/edit "Principles of Data in KBase"
[KBS2]: https://docs.google.com/a/lbl.gov/document/d/1oNWIh8yCroBqqCvok2tt6Hbx-lz9uEnBqMdoC7Ws7zw/edit?usp=sharing
