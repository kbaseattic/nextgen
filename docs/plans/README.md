# Next generation discussions and plans

## Next few months

First target is data. The data model is fundamental and is currently not serving our needs in the area of extensibility, flexibility, ease of use, and flexibility. This needs to be fundamentally re-thought and re-designed. How we do the data models and interfaces (APIs) will affect most other pieces of the system. Adam's and other existing data principles documents will be major inputs, but we want to work as bottom-up as possible in the first stages to make sure we do not build a baroque second system.

First part of this is to work on the abstract data model, using as a base some simple known scientific objects, such as assembly and maybe annotation. From there, perform prototyping using some wire protocols. The prototypes should be in a few different technologies, so we can do a "bake-off" to determine which formats make the most sense. Also think about storage. Then, back to modeling to mock up a self-contained "service" that uses several data objects at once, and to include provenance and versioning in the discussion. More prototyping, then it will be time to stop and think about more complex data objects. What I would like to build up to, as quickly as we can, is some fundamental insights into how to use concepts such as polymorphism and generics, inheritance and composition, within the KBase type system. This will be really important to have down as we move to the more complex objects, like "genome", that seem to have several isomorphs.

Other issues:
- Sharing
- Blob store (Shock)

Once these modeling concepts are understood, we can move towards the Frankenstein phase where we start building up a parallel data infrastructure for storage of the full data set, with all existing types getting moved over. This will also be the time to try some new database tech., such as MonetDB columnar storage and Hadoop/Hive/etc. indexing. Not all of this will happen in the first few months, but some of it will need to; it's unclear at this point, which-- whether Frankie is growing a new arm or extra ear, or both.

## Next year

Some of this is still data-centric -- the problem is too big to put to rest in a couple of months -- but I think there are two things that will happen in the next year. First, the data modeling Frankenstein will start getting plugged in to the full system. Probably this will require parallel scientific service interfaces, that understand the new data types, and work on a smaller demonstration set (not the full production data). This transition will no doubt raise some issues, and we'll have to spend effort on them as they arise. Second, the "services" themselves will start to 



## Three year span

I am not sure I would believe anything very specific here.

