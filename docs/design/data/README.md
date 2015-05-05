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

See [separate data sharing doc](sharing/data_sharing.asciidoc).
