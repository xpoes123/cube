# HTR subset → finish memory

Hand-extendable memory of canonical HTR subsets and their finish-move
sequences. Each entry is keyed by the canonical-subset tuple — corner
positions after DR on the listed axis — and contains the move sequence
to reach the HTR-solved (and ultimately solved) state.

This file REPLACES the binary pickle cache `subset_finish_cache.pkl`.
Humans memorize a finite set of these patterns and recall them by
sight; this file makes the memory editable, reviewable, and extensible
by a top-level FMC solver inspecting solves and adding entries.

Format: one entry per `###` block, then `axis: UD|FB|RL`, then `moves: ...`.
An empty `moves:` line means already-solved.

## Entries

### subset: (0, 1, 2, 3, 4, 5, 6, 7)

- axis: FB
- moves: ``
- axis: RL
- moves: ``
- axis: UD
- moves: ``

### subset: (0, 1, 2, 3, 4, 6, 7, 5)

- axis: UD
- moves: `R2 U F2 U' B2 U F2 U L2 D2 F2 L2 F2 U2 B2 U2 F2 U2`

### subset: (0, 1, 2, 3, 4, 7, 5, 6)

- axis: UD
- moves: `F2 U L2 U' R2 U L2 U U2 R2 F2`

### subset: (0, 1, 2, 3, 5, 7, 6, 4)

- axis: UD
- moves: `R2 U L2 U' B2 U L2 U U2 B2 U2 L2 B2 U2 R2 F2 D2 F2`

### subset: (0, 1, 2, 3, 6, 5, 7, 4)

- axis: UD
- moves: `F2 U L2 U' R2 U L2 U B2 U2 R2 F2 L2 U2 R2 D2 R2 U2`

### subset: (0, 1, 2, 4, 3, 5, 7, 6)

- axis: UD
- moves: `U L2 U' R2 U L2 U R2 F2 R2 U2 F2 U2 R2 F2 U2 R2 U2`

### subset: (0, 1, 2, 4, 3, 6, 5, 7)

- axis: UD
- moves: `U B2 U F2 U' B2 U U2 R2 F2 R2 U2 R2 U2 R2 U2 F2 R2`

### subset: (0, 1, 2, 4, 3, 7, 6, 5)

- axis: FB
- moves: `F' U2 F U2 F2 L2 F L2 F F2 D2 B2 F2 L2 D2 F2 L2 U2 R2 D2 U2`
- axis: RL
- moves: `R' U2 R U2 R2 F2 R F2 R R2 F2 R2 U2 R2 F2 U2 F2 U2 R2`
- axis: UD
- moves: `U' R2 U R2 U2 B2 U B2 U R2 D2 F2 D2 R2 F2 R2 F2`

### subset: (0, 1, 2, 4, 5, 3, 6, 7)

- axis: UD
- moves: `U R2 U' L2 U R2 U F2 D2 R2 B2 L2 U2 L2 D2 R2 U2 F2`

### subset: (0, 1, 2, 4, 6, 3, 7, 5)

- axis: UD
- moves: `U F2 U' B2 U F2 U F2 D2 F2 R2 F2 U2 L2 U2 F2 R2 U2`

### subset: (0, 1, 2, 5, 3, 4, 6, 7)

- axis: UD
- moves: `R2 U R2 U' L2 U R2 U F2 D2 R2 B2 L2 U2 L2 D2 R2 U2 F2 R2`

### subset: (0, 1, 2, 5, 3, 6, 7, 4)

- axis: UD
- moves: `F2 U F2 U L2 U2 R2 F2 U L2 U R2 B2 L2 U2 F2 D2 F2 L2`

### subset: (0, 1, 2, 5, 3, 7, 4, 6)

- axis: UD
- moves: `U2 F2 U B2 U' F2 U B2 U B2 L2 U2 F2 D2 R2 F2 R2 U2 L2 U2 R2 U2`

### subset: (0, 1, 2, 5, 4, 3, 7, 6)

- axis: UD
- moves: `U2 R2 U L2 F2 R2 B2 D R2 F2 R2 U2 F2 R2 D2 R2 F2`

### subset: (0, 1, 2, 5, 4, 7, 6, 3)

- axis: UD
- moves: `U2 R2 U F2 U R2 U' F2 U R2 U2 F2 U2 F2 R2 U2 R2 F2`

### subset: (0, 1, 2, 5, 6, 4, 7, 3)

- axis: UD
- moves: `F2 U' B2 R2 F2 L2 D L2 F2 R2 B2 U2 F2`

### subset: (0, 1, 2, 6, 3, 4, 7, 5)

- axis: UD
- moves: `U B2 U F2 U' B2 U B2 U2 F2 U2 L2 D2 R2 F2 L2 U2 R2 U2`

### subset: (0, 1, 2, 6, 3, 5, 4, 7)

- axis: FB
- moves: `F' U2 F U2 F2 L2 F L2 F F2 D2 B2 L2 D2 F2 U2 R2 U2`
- axis: RL
- moves: `R' U2 R U2 R2 F2 R F2 R D2 L2 U2 L2 F2 R2 F2 R2 D2 R2 U2`
- axis: UD
- moves: `U' R2 U R2 U2 B2 U B2 U F2 R2 D2 F2 R2 D2 R2 D2 F2 R2 F2`

### subset: (0, 1, 2, 6, 3, 7, 5, 4)

- axis: UD
- moves: `U L2 U' R2 U L2 U F2 R2 B2 U2 B2 R2 F2 L2 D2 L2 U2 R2`

### subset: (0, 1, 2, 6, 4, 3, 5, 7)

- axis: UD
- moves: `U F2 U' B2 U F2 U U2 B2`

### subset: (0, 1, 2, 6, 4, 5, 7, 3)

- axis: UD
- moves: `U R2 U L2 U' R2 U L2 U2`

### subset: (0, 1, 2, 7, 3, 4, 5, 6)

- axis: UD
- moves: `F2 U F2 U L2 U2 R2 F2 U L2 U U2 R2 U2 R2 F2 L2 F2 R2 U2`

### subset: (0, 1, 2, 7, 3, 5, 6, 4)

- axis: UD
- moves: `U2 F2 U B2 U' F2 U B2 U`

### subset: (0, 1, 2, 7, 3, 6, 4, 5)

- axis: UD
- moves: `R2 U R2 U' L2 U R2 U D2 B2 U2 R2 D2 L2 F2 R2 U2 R2 U2`

### subset: (0, 1, 2, 7, 4, 3, 6, 5)

- axis: UD
- moves: `R2 U L2 U R2 U' L2 U F2 U2 F2 R2 U2 F2 R2 F2 R2 F2`

### subset: (0, 1, 2, 7, 4, 6, 5, 3)

- axis: UD
- moves: `F2 U' B2 R2 F2 L2 D F2 R2 U2 R2 F2 D2 F2 R2 F2`

### subset: (0, 1, 2, 7, 5, 4, 6, 3)

- axis: UD
- moves: `R2 U F2 R2 F2 R2 U U2 F2 R2 U2 F2 R2 F2 R2 U2 F2`

### subset: (0, 1, 3, 2, 4, 6, 5, 7)

- axis: UD
- moves: `R2 U2 F2 U L2 F2 R2 B2 D F2 L2 D2 L2 F2 U2 F2 D2 F2 U2`

### subset: (0, 1, 3, 2, 4, 7, 6, 5)

- axis: UD
- moves: `F2 U F2 U' L2 U F2 U B2 L2 F2 D2 B2 U2 L2 U2 R2`

### subset: (0, 1, 3, 2, 5, 6, 7, 4)

- axis: UD
- moves: `F2 U R2 U' L2 U L2 F2 B2 D B2 R2 U2 R2 U2 F2 R2 F2 R2 U2 R2 U2`

### subset: (0, 1, 3, 2, 6, 4, 7, 5)

- axis: UD
- moves: `R2 U2 F2 U L2 F2 R2 B2 D B2 L2 D2 B2 D2 R2 U2 F2 R2`

### subset: (0, 1, 3, 4, 2, 5, 6, 7)

- axis: UD
- moves: `R2 U F2 U' L2 U F2 U L2 B2 F2 U2 F2 L2 U2 R2 F2 U2 B2 U2`

### subset: (0, 1, 3, 4, 2, 6, 7, 5)

- axis: UD
- moves: `R2 U R2 U F2 U2 B2 R2 U F2 U D2 F2 U2 B2 U2 L2 F2 L2 F2 D2 U2`

### subset: (0, 1, 3, 4, 2, 7, 5, 6)

- axis: UD
- moves: `F2 U B2 R2 F2 L2 D L2 U2 R2 U2 F2 R2 B2 U2 F2 U2 F2 U2`

### subset: (0, 1, 3, 5, 2, 4, 7, 6)

- axis: UD
- moves: `U B2 U' R2 U F2 R2 L2 D B2 U2 F2 U2 R2 F2 L2 U2 R2 U2 R2 U2`

### subset: (0, 1, 3, 5, 2, 7, 6, 4)

- axis: UD
- moves: `U' R2 U R2 U2 R2 B2 U B2 U D2 F2 D2 F2 R2 U2 F2 U2 F2 U2`

### subset: (0, 1, 3, 6, 2, 4, 5, 7)

- axis: UD
- moves: `R2 U R2 U F2 U2 B2 R2 U F2 U F2 D2 L2 F2 U2 R2 U2 L2 F2 U2`

### subset: (0, 1, 3, 6, 2, 5, 7, 4)

- axis: UD
- moves: `F2 U B2 R2 F2 L2 D B2 F2 R2 F2 L2`

### subset: (0, 1, 3, 6, 2, 7, 4, 5)

- axis: UD
- moves: `R2 U F2 U' L2 U F2 U U2 L2 U2 L2 F2 L2 F2 U2 R2`

### subset: (0, 1, 3, 7, 2, 5, 4, 6)

- axis: UD
- moves: `U' R2 U R2 U2 R2 B2 U B2 U D2 R2 U2 L2 F2 R2 B2 R2 U2 F2 U2`

### subset: (0, 1, 3, 7, 2, 6, 5, 4)

- axis: UD
- moves: `U B2 U' R2 U F2 R2 L2 D B2 R2 F2 L2 R2`

### subset: (0, 1, 4, 2, 3, 5, 6, 7)

- axis: UD
- moves: `U F2 U' L2 U F2 U R2 D2 B2 L2 D2 R2 F2 U2 F2 U2 L2`

### subset: (0, 1, 4, 2, 3, 6, 7, 5)

- axis: UD
- moves: `U' L2 F2 R2 B2 D U2 L2 B2 D2 R2 U2 L2 U2 F2 D2 F2 U2`

### subset: (0, 1, 4, 2, 3, 7, 5, 6)

- axis: UD
- moves: `R2 U F2 U' L2 U2 R2 B2 U' F2 U U2 B2 R2 D2 F2 R2 F2 L2 F2 D2 U2 R2`

### subset: (0, 1, 4, 3, 2, 5, 7, 6)

- axis: UD
- moves: `U2 R2 U' B2 R2 F2 L2 D F2 R2 U2 R2 F2 D2 F2 U2`

### subset: (0, 1, 4, 3, 2, 6, 5, 7)

- axis: UD
- moves: `U2 F2 U L2 F2 R2 B2 D U2 R2 F2 D2 F2 R2 U2 R2 U2`

### subset: (0, 1, 4, 3, 2, 7, 6, 5)

- axis: UD
- moves: `R2 U B2 U L2 U' B2 U U2 R2 B2 D2 B2 U2 F2 U2`

### subset: (0, 1, 4, 5, 2, 7, 3, 6)

- axis: UD
- moves: `R2 U2 F2 U' F2 R2 F2 R2 U B2 D2 R2 B2 F2 U2 L2 F2 R2 F2 U2`

### subset: (0, 1, 4, 6, 2, 5, 3, 7)

- axis: UD
- moves: `F2 U R2 U' F2 U R2 U F2 R2 F2 D2 R2 F2 R2 F2 D2 R2 U2`

### subset: (0, 1, 5, 2, 3, 6, 4, 7)

- axis: UD
- moves: `F2 U L2 U' B2 U L2 U B2 R2 D2 F2 L2 D2 R2 F2`

### subset: (0, 1, 5, 3, 2, 7, 4, 6)

- axis: UD
- moves: `U B2 U' F2 U B2 U B2 R2 B2 U2 F2 D2 L2 D2`

### subset: (0, 1, 5, 4, 2, 6, 3, 7)

- axis: UD
- moves: `F2 U B2 U' R2 U B2 U F2 U2 F2 L2 D2 R2 F2 L2 U2 B2 U2 F2 U2`

### subset: (0, 2, 1, 3, 4, 5, 7, 6)

- axis: UD
- moves: `R2 U2 F2 U' L2 F2 R2 B2 D R2 F2 U2 F2 R2 D2 R2 U2 R2`

### subset: (0, 2, 1, 3, 4, 7, 6, 5)

- axis: UD
- moves: `R2 U R2 U' F2 U R2 U F2 R2 F2 U2 R2 U2 F2 U2 F2 U2`

### subset: (0, 2, 1, 3, 5, 4, 6, 7)

- axis: UD
- moves: `R2 U2 F2 U F2 R2 F2 R2 U F2 R2 F2 U2 F2 U2 R2 F2 R2 F2`

### subset: (0, 2, 1, 3, 5, 6, 7, 4)

- axis: UD
- moves: `R2 U B2 U' F2 U F2 R2 L2 D D2 F2 D2 L2 U2 R2 B2 U2 B2 U2 R2 U2`

### subset: (0, 2, 1, 4, 3, 5, 6, 7)

- axis: UD
- moves: `U L2 U F2 U' L2 U U2 F2 R2 D2 L2 D2 R2 U2 F2`

### subset: (0, 2, 1, 4, 3, 6, 7, 5)

- axis: UD
- moves: `F2 U F2 U' L2 U2 R2 B2 U' F2 U R2 D2 L2 F2 L2 B2 D2 R2 D2 F2 R2 U2`

### subset: (0, 2, 1, 4, 3, 7, 5, 6)

- axis: UD
- moves: `U' F2 U L2 U2 R2 F2 U L2 U D2 F2 U2 R2 F2 R2 B2 U2 R2 U2 R2`

### subset: (0, 2, 1, 4, 5, 3, 7, 6)

- axis: UD
- moves: `U L2 U' B2 U R2 F2 B2 D U2 F2 U2 B2 R2 B2 L2 U2 F2 U2 F2`

### subset: (0, 2, 1, 4, 6, 5, 7, 3)

- axis: UD
- moves: `U B2 R2 F2 L2 D U2 B2 U2 F2 L2 B2 R2 U2 F2 U2`

### subset: (0, 2, 1, 5, 3, 6, 4, 7)

- axis: UD
- moves: `R2 U F2 U F2 U2 F2 R2 U R2 U L2 F2 D2 F2 R2 D2 U2 B2 U2 L2`

### subset: (0, 2, 1, 5, 3, 7, 6, 4)

- axis: UD
- moves: `U2 R2 U' R2 F2 R2 F2 U R2 U2 F2 U2 F2 R2 F2 R2 U2 F2`

### subset: (0, 2, 1, 5, 4, 3, 6, 7)

- axis: UD
- moves: `U2 F2 U F2 R2 F2 R2 U F2 R2 F2 U2 F2 U2 R2 F2 R2 F2 R2`

### subset: (0, 2, 1, 6, 3, 4, 5, 7)

- axis: UD
- moves: `F2 U F2 U' L2 U2 R2 B2 U' F2 U L2 D2 L2 U2 F2 L2 R2 D2 F2`

### subset: (0, 2, 1, 6, 3, 5, 7, 4)

- axis: UD
- moves: `U' F2 U L2 U2 R2 F2 U L2 U R2 U2 L2 D2 B2 D2 F2 R2`

### subset: (0, 2, 1, 6, 3, 7, 4, 5)

- axis: UD
- moves: `U L2 U F2 U' L2 U B2 U2 L2 D2 R2 B2 R2 F2 U2 R2 D2 U2`

### subset: (0, 2, 1, 6, 4, 3, 7, 5)

- axis: UD
- moves: `F2 U R2 U L2 U2 L2 F2 U R2 U L2 D2 B2 L2 D2 R2 U2 R2 F2`

### subset: (0, 2, 1, 6, 4, 7, 5, 3)

- axis: UD
- moves: `U B2 R2 F2 L2 D F2 L2 R2 U2 R2 F2 D2 F2 R2 U2 L2`

### subset: (0, 2, 1, 6, 5, 4, 7, 3)

- axis: UD
- moves: `U R2 U B2 U' L2 F2 B2 D L2 D2 R2 D2 B2 D2 U2 L2 U2 F2`

### subset: (0, 2, 1, 7, 3, 4, 6, 5)

- axis: UD
- moves: `R2 U F2 U F2 U2 F2 R2 U R2 U U2 R2 F2 R2 U2 F2 U2`

### subset: (0, 2, 1, 7, 3, 5, 4, 6)

- axis: UD
- moves: `U2 R2 U' R2 F2 R2 F2 U U2 L2 F2 L2 R2 D2 B2 D2 F2 U2 R2`

### subset: (0, 2, 1, 7, 4, 5, 6, 3)

- axis: UD
- moves: `F2 U R2 F2 R2 F2 U U2 R2 F2 U2 R2 F2 R2 F2 U2 R2`

### subset: (0, 2, 1, 7, 5, 3, 6, 4)

- axis: UD
- moves: `R2 U L2 U' R2 U R2 F2 B2 D F2 R2 B2 D2 B2 D2 L2 U2 F2 U2`

### subset: (0, 3, 1, 4, 5, 2, 6, 7)

- axis: UD
- moves: `F2 U R2 U' F2 U R2 U F2 R2 U2 F2 R2 U2 R2 F2`

### subset: (0, 3, 1, 4, 5, 6, 7, 2)

- axis: UD
- moves: `R2 U' L2 F2 R2 B2 D L2 F2 R2 B2 U2 R2 F2 R2 F2 R2`

### subset: (0, 3, 1, 4, 6, 2, 7, 5)

- axis: UD
- moves: `U2 R2 U R2 U L2 U' R2 U B2 D2 L2 D2 L2 B2 U2 R2 U2 L2`

### subset: (0, 3, 1, 5, 4, 2, 7, 6)

- axis: UD
- moves: `R2 U R2 U L2 U2 L2 F2 U R2 U R2 B2 U2 L2 U2 L2 B2 U2 F2`

### subset: (0, 3, 1, 5, 4, 7, 6, 2)

- axis: UD
- moves: `U B2 U L2 U' B2 U U2 R2 D2 R2 B2 L2 B2 U2 R2 D2 R2 U2`

### subset: (0, 3, 1, 5, 6, 4, 7, 2)

- axis: UD
- moves: `U' L2 F2 R2 B2 D D2 F2 D2 L2 F2 R2 B2 U2 F2`

### subset: (0, 3, 1, 6, 4, 2, 5, 7)

- axis: UD
- moves: `U2 R2 U R2 U L2 U' R2 U F2 D2 B2 D2 F2 L2 F2 R2 F2 U2 R2`

### subset: (0, 3, 1, 6, 4, 5, 7, 2)

- axis: UD
- moves: `U2 F2 U F2 U' B2 U F2 U F2 D2 F2 R2 F2 U2 L2 U2 F2 R2 U2 F2 U2`

### subset: (0, 3, 1, 6, 5, 2, 7, 4)

- axis: UD
- moves: `U2 R2 U' B2 R2 F2 L2 D D2 F2 U2 L2 F2 R2 B2 D2 R2 F2 U2`

### subset: (0, 3, 1, 7, 4, 2, 6, 5)

- axis: UD
- moves: `U F2 U' L2 U F2 U L2 D2 F2 U2 R2 B2 L2 U2 R2 F2 U2`

### subset: (0, 3, 1, 7, 4, 6, 5, 2)

- axis: UD
- moves: `U' L2 F2 R2 B2 D D2 R2 F2 U2 R2 F2 D2 F2 R2 U2`

### subset: (0, 4, 1, 6, 5, 3, 7, 2)

- axis: UD
- moves: `R2 U R2 U F2 U2 B2 R2 U F2 U B2 F2 R2 D2 R2 U2 F2 L2`

### subset: (0, 4, 1, 7, 5, 2, 6, 3)

- axis: UD
- moves: `U' R2 U R2 U2 R2 B2 U B2 U B2 R2 D2 F2 U2 B2 L2 D2 U2 F2 R2 U2`

### subset: (1, 0, 2, 3, 4, 6, 5, 7)

- axis: UD
- moves: `R2 U2 F2 U' B2 R2 F2 L2 D D2 F2 R2 F2 U2 R2 F2 D2 F2`

### subset: (1, 0, 2, 3, 4, 7, 6, 5)

- axis: UD
- moves: `F2 U R2 U' L2 U R2 U R2 D2 R2 B2 D2 B2 R2 B2 U2 L2 U2 R2 U2`

### subset: (1, 0, 2, 3, 5, 6, 7, 4)

- axis: UD
- moves: `F2 U F2 U' L2 U B2 R2 L2 D B2 D2 L2 B2 L2 U2 L2 D2 F2 U2`

### subset: (1, 0, 2, 3, 6, 4, 7, 5)

- axis: UD
- moves: `R2 U2 F2 U' B2 R2 F2 L2 D D2 U2 R2 B2 F2 U2 B2 D2`

### subset: (1, 0, 2, 4, 3, 5, 6, 7)

- axis: UD
- moves: `U B2 U' R2 U B2 U R2 F2 D2 B2 D2 F2 U2 R2 U2`

### subset: (1, 0, 2, 4, 3, 6, 7, 5)

- axis: UD
- moves: `U' R2 U F2 U2 B2 R2 U F2 U R2 F2 R2 F2 U2 B2 U2 F2 U2 R2 U2`

### subset: (1, 0, 2, 4, 5, 3, 7, 6)

- axis: UD
- moves: `U F2 U' L2 U B2 R2 L2 D B2 L2 U2 B2 R2 F2 U2 F2 D2 R2 U2`

### subset: (1, 0, 2, 4, 5, 7, 6, 3)

- axis: UD
- moves: `U' R2 F2 R2 F2 U R2 U2 R2 F2 R2 F2 U2 R2`

### subset: (1, 0, 2, 5, 3, 4, 7, 6)

- axis: UD
- moves: `R2 U F2 U' L2 U B2 R2 L2 D D2 R2 F2 U2 R2 U2 R2 U2 F2 D2 F2`

### subset: (1, 0, 2, 5, 3, 6, 4, 7)

- axis: UD
- moves: `F2 U F2 R2 F2 R2 U B2 R2 B2 F2 D2 L2 D2 R2 U2 F2 U2`

### subset: (1, 0, 2, 5, 3, 7, 6, 4)

- axis: UD
- moves: `R2 U R2 U R2 U2 R2 B2 U B2 U B2 R2 D2 F2 U2 B2 L2 D2 U2 F2`

### subset: (1, 0, 2, 5, 4, 3, 6, 7)

- axis: UD
- moves: `U2 R2 U' F2 R2 F2 R2 U F2 R2 U2 F2 R2 F2 R2 U2 F2 U2`

### subset: (1, 0, 2, 5, 4, 6, 7, 3)

- axis: UD
- moves: `R2 U B2 U L2 U' F2 R2 L2 D U2 R2 U2 L2 B2 R2 F2 R2`

### subset: (1, 0, 2, 5, 6, 3, 7, 4)

- axis: UD
- moves: `F2 U R2 U' F2 U L2 F2 B2 D U2 F2 D2 B2 L2 F2 R2 U2 F2 D2`

### subset: (1, 0, 2, 6, 3, 4, 5, 7)

- axis: UD
- moves: `U' R2 U F2 U2 B2 R2 U F2 U L2 D2 L2 F2 R2 F2 U2 B2 U2 R2`

### subset: (1, 0, 2, 6, 3, 7, 4, 5)

- axis: UD
- moves: `U B2 U' R2 U B2 U B2 U2 L2 B2 R2 B2 D2 F2 U2 R2 D2 U2`

### subset: (1, 0, 2, 6, 4, 3, 7, 5)

- axis: UD
- moves: `U L2 F2 R2 B2 D B2 L2 B2 F2 D2 L2 F2 D2 R2 B2 U2`

### subset: (1, 0, 2, 6, 5, 4, 7, 3)

- axis: UD
- moves: `U B2 U L2 U' F2 R2 L2 D L2 F2 D2 R2 D2 L2 U2 F2 D2 F2 R2 U2`

### subset: (1, 0, 2, 7, 3, 4, 6, 5)

- axis: UD
- moves: `F2 U F2 R2 F2 R2 U R2 U2 F2 R2 F2 R2 U2 R2 U2 F2`

### subset: (1, 0, 2, 7, 3, 5, 4, 6)

- axis: UD
- moves: `R2 U R2 U R2 U2 R2 B2 U B2 U R2 U2 F2 L2 D2 B2 L2 F2 U2`

### subset: (1, 0, 2, 7, 3, 6, 5, 4)

- axis: UD
- moves: `R2 U F2 U' L2 U B2 R2 L2 D L2 B2 L2 F2 R2 U2 F2 U2 R2 U2 F2 U2`

### subset: (1, 0, 2, 7, 4, 3, 5, 6)

- axis: UD
- moves: `F2 U R2 U' F2 U L2 F2 B2 D B2 D2 L2 B2 D2 F2 R2 U2 L2`

### subset: (1, 0, 2, 7, 4, 5, 6, 3)

- axis: UD
- moves: `R2 U' R2 F2 R2 F2 U F2 R2 U2 F2 R2 F2 U2 F2 U2 R2 U2`

### subset: (1, 0, 3, 2, 4, 6, 7, 5)

- axis: UD
- moves: `R2 U L2 U' B2 U R2 F2 B2 D R2 F2 L2 B2 D2 L2 F2 D2 R2 B2 U2`

### subset: (1, 0, 3, 2, 4, 7, 5, 6)

- axis: UD
- moves: `F2 U B2 U' R2 U F2 R2 L2 D F2 L2 B2 L2 D2 B2 R2 D2 F2 L2 U2`

### subset: (1, 0, 3, 2, 5, 4, 7, 6)

- axis: UD
- moves: `U R2 L2 F2 B2 D R2 F2 L2 B2 U2 R2 U2 R2 F2 R2 F2 U2 R2 U2`

### subset: (1, 0, 3, 2, 5, 7, 6, 4)

- axis: UD
- moves: `R2 U F2 U' B2 U B2 R2 L2 D F2 R2 B2 U2 R2 F2 D2 R2 F2 U2 R2`

### subset: (1, 0, 3, 2, 6, 5, 7, 4)

- axis: UD
- moves: `F2 U B2 U' R2 U F2 R2 L2 D F2 D2 B2 U2 L2 U2 R2 F2 L2 U2`

### subset: (1, 0, 3, 4, 2, 5, 7, 6)

- axis: UD
- moves: `R2 U R2 U' L2 U L2 F2 B2 D U2 L2 B2 U2 L2 B2 U2 L2 F2`

### subset: (1, 0, 3, 4, 2, 7, 6, 5)

- axis: UD
- moves: `F2 U F2 U F2 U2 F2 R2 U R2 U F2 U2 F2 U2 F2 R2 F2 R2 F2 U2 R2`

### subset: (1, 0, 3, 5, 2, 4, 6, 7)

- axis: UD
- moves: `U L2 U' R2 U R2 F2 B2 D F2 R2 D2 B2 L2 U2 F2 R2 U2 R2`

### subset: (1, 0, 3, 5, 2, 7, 4, 6)

- axis: UD
- moves: `U B2 U F2 U' F2 R2 L2 D U2 F2 D2 F2 L2 U2 F2 L2 U2 F2 R2 U2`

### subset: (1, 0, 3, 6, 2, 5, 4, 7)

- axis: UD
- moves: `F2 U F2 U F2 U2 F2 R2 U R2 U F2 D2 R2 U2 L2 B2 D2 R2 U2 L2`

### subset: (1, 0, 3, 6, 2, 7, 5, 4)

- axis: UD
- moves: `R2 U R2 U' L2 U L2 F2 B2 D L2 B2 L2 D2 L2 D2 F2 U2 R2 U2`

### subset: (1, 0, 3, 7, 2, 5, 6, 4)

- axis: UD
- moves: `U B2 U F2 U' F2 R2 L2 D B2 D2 B2 F2 L2 D2 F2 D2 F2 R2 U2`

### subset: (1, 0, 3, 7, 2, 6, 4, 5)

- axis: UD
- moves: `U L2 U' R2 U R2 F2 B2 D B2 R2 D2 R2 D2 F2 L2 R2 U2 R2 U2`

### subset: (1, 0, 4, 2, 3, 5, 7, 6)

- axis: UD
- moves: `U R2 U' L2 U L2 F2 B2 D F2 U2 F2 U2 R2 U2 R2 F2 U2 B2 U2 R2 U2`

### subset: (1, 0, 4, 2, 3, 6, 5, 7)

- axis: UD
- moves: `U B2 U' F2 U F2 R2 L2 D U2 R2 U2 F2 D2 B2 R2 F2 U2`

### subset: (1, 0, 4, 3, 2, 5, 6, 7)

- axis: UD
- moves: `U2 R2 U R2 F2 R2 F2 U U2 F2 R2 U2 F2 R2 F2 U2 F2 U2 R2`

### subset: (1, 0, 4, 3, 2, 7, 5, 6)

- axis: UD
- moves: `F2 U L2 U' B2 U R2 F2 B2 D U2 R2 D2 R2 U2 B2 R2 U2 F2 U2 B2`

### subset: (1, 0, 4, 5, 2, 6, 3, 7)

- axis: UD
- moves: `F2 U L2 U' R2 U R2 F2 B2 D U2 B2 R2 B2 F2 D2 F2 R2 U2`

### subset: (1, 0, 4, 6, 2, 7, 3, 5)

- axis: UD
- moves: `F2 U' F2 R2 F2 R2 U D2 B2 F2 L2 B2 F2 D2 F2 U2 R2 U2`

### subset: (1, 0, 4, 7, 2, 5, 3, 6)

- axis: UD
- moves: `U F2 U' B2 U B2 R2 L2 D L2 F2 R2 F2 R2 U2 F2 R2 U2 R2 F2 U2`

### subset: (1, 0, 5, 2, 3, 7, 4, 6)

- axis: UD
- moves: `U2 F2 U R2 F2 R2 F2 U R2 D2 L2 U2 R2 B2 L2 R2 D2 F2`

### subset: (1, 0, 5, 3, 2, 6, 4, 7)

- axis: UD
- moves: `R2 U F2 U R2 U2 L2 B2 U F2 U L2 D2 R2 D2 B2 R2 B2 U2 B2`

### subset: (1, 0, 5, 4, 2, 7, 3, 6)

- axis: UD
- moves: `R2 U2 F2 U R2 F2 R2 F2 U R2 D2 F2 L2 B2 L2 F2 D2`

### subset: (2, 0, 3, 1, 4, 5, 7, 6)

- axis: UD
- moves: `R2 U2 F2 U' L2 F2 R2 B2 D L2 B2 D2 L2 D2 F2 U2 R2 F2 U2`

### subset: (2, 0, 3, 1, 4, 7, 6, 5)

- axis: UD
- moves: `R2 U R2 U' F2 U R2 U R2 F2 R2 U2 R2 U2 F2 U2 F2`

### subset: (2, 0, 3, 1, 5, 4, 6, 7)

- axis: UD
- moves: `R2 U2 F2 U F2 R2 F2 R2 U U2 R2 U2 R2 F2 U2 R2 F2 R2`

### subset: (2, 0, 3, 1, 5, 6, 7, 4)

- axis: UD
- moves: `R2 U B2 U' F2 U F2 R2 L2 D B2 U2 F2 R2 D2 F2 R2 U2 B2`

### subset: (2, 0, 3, 4, 1, 5, 6, 7)

- axis: UD
- moves: `U L2 U F2 U' L2 U F2 D2 L2 D2 R2 F2 R2 F2 U2 R2`

### subset: (2, 0, 3, 4, 1, 6, 7, 5)

- axis: UD
- moves: `F2 U F2 U' L2 U2 R2 B2 U' F2 U R2 U2 L2 U2 B2 U2 F2`

### subset: (2, 0, 3, 4, 1, 7, 5, 6)

- axis: UD
- moves: `U' F2 U L2 U2 R2 F2 U L2 U L2 D2 R2 U2 F2 U2 B2 R2`

### subset: (2, 0, 3, 5, 1, 6, 4, 7)

- axis: UD
- moves: `R2 U F2 U F2 U2 F2 R2 U R2 U D2 B2 F2 L2 F2 L2 U2 B2 D2`

### subset: (2, 0, 3, 5, 1, 7, 6, 4)

- axis: UD
- moves: `U2 R2 U' R2 F2 R2 F2 U U2 R2 F2 U2 F2 U2 F2 U2 R2`

### subset: (2, 0, 3, 6, 1, 4, 5, 7)

- axis: UD
- moves: `F2 U F2 U' L2 U2 R2 B2 U' F2 U R2 U2 L2 F2 L2 B2 U2 R2 D2 F2 R2 U2`

### subset: (2, 0, 3, 6, 1, 5, 7, 4)

- axis: UD
- moves: `U' F2 U L2 U2 R2 F2 U L2 U D2 F2 D2 R2 F2 R2 B2 D2 R2 U2 R2`

### subset: (2, 0, 3, 6, 1, 7, 4, 5)

- axis: UD
- moves: `U L2 U F2 U' L2 U U2 B2 R2 B2 F2 U2 R2 U2 R2 U2 F2`

### subset: (2, 0, 3, 7, 1, 4, 6, 5)

- axis: UD
- moves: `R2 U F2 U F2 U2 F2 R2 U R2 U R2 F2 U2 F2 R2 F2 U2 R2`

### subset: (2, 0, 3, 7, 1, 5, 4, 6)

- axis: UD
- moves: `U2 R2 U' R2 F2 R2 F2 U L2 D2 F2 U2 F2 L2 F2 R2 U2 F2 D2 U2`

### subset: (2, 0, 4, 1, 3, 5, 6, 7)

- axis: UD
- moves: `U R2 U' F2 U R2 U F2 R2 U2 F2 R2 U2 R2`

### subset: (2, 0, 4, 1, 3, 6, 7, 5)

- axis: UD
- moves: `F2 U R2 U L2 U2 L2 F2 U R2 U R2 D2 R2 B2 L2 U2 F2 U2 B2 U2`

### subset: (2, 0, 4, 1, 3, 7, 5, 6)

- axis: UD
- moves: `U B2 R2 F2 L2 D B2 U2 R2 D2 F2 U2 R2 F2 R2 B2 R2 U2`

### subset: (2, 0, 4, 3, 1, 5, 7, 6)

- axis: UD
- moves: `U B2 R2 F2 L2 D L2 B2 L2 D2 L2 F2 U2 R2 B2 U2 R2`

### subset: (2, 0, 4, 3, 1, 6, 5, 7)

- axis: UD
- moves: `F2 U R2 U L2 U2 L2 F2 U R2 U B2 U2 L2 F2 L2 B2 R2 D2 F2 R2 U2`

### subset: (2, 0, 4, 3, 1, 7, 6, 5)

- axis: UD
- moves: `U R2 U' F2 U R2 U F2 U2 R2 U2 R2 F2 R2 U2 F2 R2`

### subset: (2, 0, 4, 5, 1, 7, 3, 6)

- axis: UD
- moves: `F2 U R2 F2 R2 F2 U B2 U2 L2 D2 F2 D2 R2 F2 L2 R2`

### subset: (2, 0, 4, 6, 1, 5, 3, 7)

- axis: UD
- moves: `R2 U R2 U' F2 U R2 U R2 D2 R2 F2 R2 F2 D2 F2 U2 F2 R2 U2`

### subset: (2, 0, 4, 7, 1, 6, 3, 5)

- axis: UD
- moves: `U2 F2 U F2 R2 F2 R2 U B2 D2 R2 U2 L2 B2 R2 U2 B2 R2 U2`

### subset: (2, 0, 5, 1, 3, 6, 4, 7)

- axis: UD
- moves: `U2 R2 U L2 U R2 U' L2 U F2 D2 R2 U2 L2 B2 D2 R2 U2 L2`

### subset: (2, 0, 5, 3, 1, 7, 4, 6)

- axis: UD
- moves: `R2 U B2 U' R2 U B2 U F2 U2 L2 B2 L2 B2 U2 F2 U2`

### subset: (2, 0, 5, 4, 1, 6, 3, 7)

- axis: UD
- moves: `U2 F2 U L2 U' B2 U L2 U D2 R2 D2 B2 R2 F2 L2 D2 R2 U2`

### subset: (3, 0, 4, 1, 2, 5, 7, 6)

- axis: UD
- moves: `F2 U L2 U' B2 U R2 F2 B2 D U2 F2 U2 B2 R2 B2 L2 U2 F2 U2`

### subset: (3, 0, 4, 1, 2, 7, 6, 5)

- axis: UD
- moves: `U2 R2 U R2 F2 R2 F2 U R2 F2 R2 U2 F2 U2 F2 R2 U2 R2`

### subset: (3, 0, 4, 2, 1, 6, 7, 5)

- axis: UD
- moves: `U B2 U' F2 U F2 R2 L2 D U2 R2 D2 B2 R2 B2 U2 B2 U2 F2 U2 R2`

### subset: (3, 0, 4, 2, 1, 7, 5, 6)

- axis: UD
- moves: `U R2 U' L2 U L2 F2 B2 D L2 B2 D2 L2 F2 U2 R2 B2 U2 R2`

### subset: (3, 0, 4, 5, 1, 6, 2, 7)

- axis: UD
- moves: `U F2 U B2 U' B2 R2 L2 D D2 L2 F2 D2 F2 R2 F2 R2 D2 R2 U2`

### subset: (3, 0, 4, 6, 1, 7, 2, 5)

- axis: UD
- moves: `U2 F2 U' L2 F2 R2 B2 D B2 D2 R2 U2 R2 U2 B2 D2 U2 R2`

### subset: (3, 0, 4, 7, 1, 5, 2, 6)

- axis: UD
- moves: `F2 U B2 U' R2 U F2 R2 L2 D B2 R2 B2 D2 R2 F2 D2 L2 B2 U2 R2`

### subset: (3, 0, 5, 1, 2, 7, 4, 6)

- axis: UD
- moves: `U' R2 F2 R2 F2 U D2 F2 U2 B2 U2 R2 F2 U2 L2 U2 R2`

### subset: (3, 0, 5, 2, 1, 6, 4, 7)

- axis: UD
- moves: `U2 R2 U' F2 R2 F2 R2 U B2 D2 L2 U2 L2 U2 F2 D2 B2`

### subset: (4, 0, 5, 2, 1, 7, 3, 6)

- axis: UD
- moves: `R2 U R2 U R2 U2 R2 B2 U B2 U F2 D2 R2 D2 F2 L2 U2 B2 L2`

### subset: (4, 0, 5, 3, 1, 6, 2, 7)

- axis: UD
- moves: `U' R2 U F2 U2 B2 R2 U F2 U F2 R2 F2 L2 D2 F2 R2 D2 F2 L2 R2`
