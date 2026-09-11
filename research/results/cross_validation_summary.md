# 5-Fold Cross-Validation Results — Topic Mapping

Gold set: 326 samples | Folds: 5 | Seed: 42

## Pooled Results (mean ± std across folds)

| Model | Pool Top1 | Pool Top3 | OS Top1 | CN Top1 | DBMS Top1 |
|:---|:---:|:---:|:---:|:---:|:---:|
| Base Hybrid | 0.5947 ± 0.0633 | 0.7391 ± 0.0257 | 0.5185 ± 0.0454 | 0.7046 ± 0.0917 | 0.6005 ± 0.1214 |
| Clean-97 FT Hybrid | 0.6346 ± 0.0732 | 0.8190 ± 0.0329 | 0.5926 ± 0.0693 | 0.7386 ± 0.1011 | 0.6009 ± 0.0990 |

## Per-Subject Top3 Accuracy (mean ± std)

| Model | OS Top3 | CN Top3 | DBMS Top3 |
|:---|:---:|:---:|:---:|
| Base Hybrid | 0.6518 ± 0.0497 | 0.8745 ± 0.0486 | 0.7371 ± 0.0754 |
| Clean-97 FT Hybrid | 0.8148 ± 0.0741 | 0.9085 ± 0.0530 | 0.7471 ± 0.0725 |

## Per-Fold Detail

| Fold | Model | n_test | Pool Top1 | Pool Top3 |
|:---:|:---|:---:|:---:|:---:|
| 1 | Base Hybrid | 66 | 0.6364 | 0.7576 |
| 1 | Clean-97 FT Hybrid | 66 | 0.6667 | 0.8333 |
| 2 | Base Hybrid | 66 | 0.6818 | 0.7727 |
| 2 | Clean-97 FT Hybrid | 66 | 0.7424 | 0.8485 |
| 3 | Base Hybrid | 66 | 0.5303 | 0.7121 |
| 3 | Clean-97 FT Hybrid | 66 | 0.5606 | 0.7727 |
| 4 | Base Hybrid | 64 | 0.5781 | 0.7344 |
| 4 | Clean-97 FT Hybrid | 64 | 0.6250 | 0.8438 |
| 5 | Base Hybrid | 64 | 0.5469 | 0.7188 |
| 5 | Clean-97 FT Hybrid | 64 | 0.5781 | 0.7969 |