# Mode: image

The source is one or more images of the object. Freedom: **high**: the guide is *one possible way* to build it, and says so at the top.

1. **Read the image**: what it is, style (low-poly, stylised, realistic, mechanical part), the view (front, 3/4, side) and what is not visible.
2. **Parts map**: split it into parts (about 8 main parts at most; group small details or leave them for a second pass). For each part: number, name, base shape or sketch, main technique, what it is attached to, difficulty. Put this table near the top of the guide.
3. **Scale**: real dimensions from something of known size in the image, or a size that makes sense for the object; say which one you used.
4. **Order**: big to small. Phase 1 is a blockout (all parts as base shapes or simple bodies with a table of position and size), then one phase per part, then materials or finishing, then clean-up and export.
5. **Hidden sides**: state the decision taken ("the back is not visible: we make it flat") so the person can change it.
6. Almost every section is `Source: proposed`; say so once at the top instead of repeating why.

Also output, at the very end of your answer, a fenced ```json block with the parts and their approximate boxes in the image (fractions 0-1 of width and height), for drawing a numbered parts map:
`{"parts":[{"n":1,"name":"Box","box":[x0,y0,x1,y1]}, ...]}`
