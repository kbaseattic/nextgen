# Next generation discussions and plans

## Next few months

### Data

#### Rationale

The data model is fundamental and is currently not serving our needs in the area of extensibility, flexibility, and performance. How we do the data models and interfaces (APIs) will affect most other pieces of the system (_e.g._, the sharing model affects UI, data protocols affect services, data storage affects search). Adam's and other existing data principles documents ([1][PoDKB]) will be major inputs, but we want to work as bottom-up as possible in the first stages to make sure we do not build a baroque second system. The working process is to roughly alternate between short cycles, 1-3 days, of design and prototyping.

#### Approach

* Start with the abstract data model, using as a base some simple known scientific objects, such as assembly and maybe annotation. Include all aspects of the data touched on in Adam's [document][PoDKB], including metadata, provenance, and sharing.
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

Some of this is still data-centric -- the problem is too big to put to rest in a couple of months -- but I think there are two things that will happen in the next year. First, the data modeling Frankenstein will start getting plugged in to the full system. Probably this will require parallel scientific service interfaces, that understand the new data types, and work on a smaller demonstration set (not the full production data). This transition will no doubt raise some issues, and we'll have to spend effort on them as they arise. Second, the "services" themselves will start to 



## Three year span

I am not sure I would believe anything very specific here.

# References

[PodKB]: https://docs.google.com/a/lbl.gov/document/d/1YY7JwAdQY2bLWZl-VtTPV_K9erA8Vkak5NdXOVUQavQ/edit "Principles of Data in KBase"
