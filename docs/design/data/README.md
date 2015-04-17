# Data design

This top-level document summarizes the data redesign. As some of the sub-sections get longer and more involved with implementations, they will get moved into their own documents and links will be added.

See also the list of [challenges](/docs/challenges/data.md) that motivate the redesign.

A number of data design docs are also in the [data_api](https://github.com/kbase/data_api) repository.

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

ASCII ER diagram:
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

We noted that all this sharing stuff could be circumvented by downloading the raw data. You _could_ prevent download of the data as part of the sharing model, but it does mean that you have to go down a much more complicated path of defining individual policies for how data can be used, no just also shared with others.  But at least having the non-transitive share would tell your collaborator that they would need to circumvent your wishes to share the data, which yes bad users could do bad things, but the social aspect would help reinforce that.  I think this point in particular is worth talking to more people about.
