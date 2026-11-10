# TP53 on T2T-CHM13: Three-Channel Echo-State

By Tyree Jones (tyofthestarz). Framework reading: [PHI_READING.md](PHI_READING.md).

## Measurement
- Reference: T2T-CHM13v2.0 (GCF_009914755.1)
- TP53 interval: NC_060941.1:7,572,544–7,591,594
- Alignment: splice-aware minimap2, MAPQ ≥ 20
- Channels (ENCODE):
  - [ENCSR985WSV](https://www.encodeproject.org/experiments/ENCSR985WSV/): dorsolateral prefrontal cortex
  - [ENCSR534OAS](https://www.encodeproject.org/experiments/ENCSR534OAS/): liver
  - [ENCSR000CUT](https://www.encodeproject.org/experiments/ENCSR000CUT/): peripheral-blood-derived mononuclear cells

## Results

| Channel | Primary mapped reads | TP53 reads (MAPQ ≥ 20) | TP53 read-CPM | Active echo amplitude | Active echo power |
|---|---:|---:|---:|---:|---:|
| Cortex | 39,201,424 | 105 | 2.678474 | 1.105510 | 1.222153 |
| Liver | 43,508,728 | 510 | 11.721786 | 2.312682 | 5.348500 |
| Blood-derived mononuclear cells | 177,015,559 | 1,311 | 7.406129 | 1.838293 | 3.379321 |

Pooled TP53 CPM = 1926 / 259,725,711 × 10⁶ = 7.415515

Merged state, using A₀ = √CPM and θ = 2π/φ² = 137.507764050°:
Ψ = [−2.007961923, 1.546457964 + 0.996028135i], active amplitude 1.839457605, active power 3.383604279.

Ordering: Liver > Blood-derived mononuclear cells > Cortex.

Notes: these are read-level CPM proxies, not TPM. The blood channel is mononuclear-cell RNA-seq, not whole-blood RNA-seq.

## Reproduce
```
python3 merge_echo_states.py
```
Reads `cortex.t2t.json`, `liver.t2t.json`, `mononuclear.t2t.json` and writes `merged_tp53_echo.json`.
