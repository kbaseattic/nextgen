# Data design

This top-level document summarizes the data redesign. As some of the sub-sections get longer and more involved with implementations, they will get moved into their own documents and links will be added.

See also the list of [challenges](/docs/challenges/data.md) that motivate the redesign.

## Information we need for each "object"

* Object metadata
  - id (hash)
  - owner
* Datum (bytes)
  - Type
* Metadata (non-computable)
* Links/references
  - Derived-from
  - Other, named, links
* Provenance (computable) -- special metadata in addition to derived-from tree
* Path, replacing current 'name' with: owner/project[/subprojects..]/name

ASCII O/R diagram:
```
                               name   id      id           
e.g., owner/project/../name     ^     ^       ^            
              +                 |     |       |            
              |                ++-----+--+ +--+---------+  
           +--+---------+      |Reference| |Derived|from|  
           | Path (name)|      ++--------+ ++-----------+  
           +------------+     * ^           ^ 1+           
                  ^--------+    |         +-+              
                           |  1 |        1|                
             +--------+ 1  |  1 +---------+1    *+------+  
             |Metadata| <-------+  Object +----> |Datum |  
             +--------+    |    ++-----+--+      +-----++  
                           |   * |     | 1     1 |     | * 
            +------------+ |     |     |         |     |   
            | Provenance <-+   1 v     v 1     + v     v 1 
            +------------+ 1   owner  id        value  type
```
## Sharing

Issue: When user Alice shares X with Bob, and Bob derives Y from X and shares Y with Carol, then in order to see the full provenance of Y the system needs to let Carol see X, whether or not Alice has shared it with her directly.

Solution: Sharing is transitive across Derived-from links without regard to object permissions, so that in the example above Carol can always see X if she has permission to see Y. This preserves transparency. However, users have the option to do another kind of sharing, which we called "radius 1" but I would now call "non-transitive". If Alice shared X non-transitively with Bob, then Bob could create Y but could not share Y with anyone else.

Put another way, imagine a `share(obj, person)` operation with a `transitive` flag on an object. Then, the following sequence is legal:

    Alice: x.transitive = True
    Alice: share(x, 'Bob')
    Bob: y = f(x)
    Bob: share(y, 'Carol') 

But, the following sequence is not:

    Alice: x.transitive = False
    Alice: share(x, 'Bob')
    Bob: y = f(x)
    Bob: share(y, 'Carol') # ERROR! 

Note that in this discussion, the "object" could be some collection of objects, e.g. a subpath of the Path described above. Also, individual people might be replaced by groups of people, or roles in a RBAC model.

This was not discussed, but while writing this it occurred to me (Dan) that we could store the transitivity of sharing as a property of the object (or subpath) itself, rather than making this a property of each individual sharing. This would make it easier to preserve this property in copies, for example.

We noted that all this sharing stuff is eminently circumventable by simply downloading the raw data.
