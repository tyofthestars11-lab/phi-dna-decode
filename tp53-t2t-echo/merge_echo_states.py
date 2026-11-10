#!/usr/bin/env python3
import json, math
from pathlib import Path

PHI = (1 + math.sqrt(5)) / 2
THETA = 2 * math.pi / (PHI ** 2)
ALPHA = math.radians(32.78439509088443)
base = Path(__file__).parent
names = ['cortex.t2t.json', 'liver.t2t.json', 'mononuclear.t2t.json']
rows = [json.loads((base / n).read_text()) for n in names]

total_primary = sum(x['primary_mapped_reads'] for x in rows)
total_tp53 = sum(x['tp53_reads_mapq_ge_threshold'] for x in rows)
pooled_cpm = total_tp53 / total_primary * 1e6
A0 = math.sqrt(pooled_cpm)
z0 = A0 * math.cos(THETA)
z1 = A0 * complex(math.cos(ALPHA), math.sin(ALPHA)) * math.sin(THETA)
mean_active_amp = sum(x['active_echo_amplitude'] for x in rows) / len(rows)
mean_active_power = sum(x['active_echo_power'] for x in rows) / len(rows)
report = {
    'reference': 'T2T-CHM13v2.0 GCF_009914755.1',
    'tp53_interval': rows[0]['tp53_interval'],
    'samples': rows,
    'merged_definition': 'Pooled direct-read signal: sum TP53 MAPQ>=20 reads divided by sum primary mapped reads.',
    'total_primary_mapped_reads': total_primary,
    'total_tp53_reads_mapq_ge_20': total_tp53,
    'pooled_tp53_read_cpm': pooled_cpm,
    'phi': PHI,
    'golden_angle_transition_degrees': math.degrees(THETA),
    'alpha_degrees': math.degrees(ALPHA),
    'pooled_input_amplitude_sqrt_read_cpm': A0,
    'pooled_echo_state': {'channel0_real': z0, 'channel1_real': z1.real, 'channel1_imag': z1.imag},
    'pooled_active_echo_amplitude': abs(z1),
    'pooled_active_echo_power': abs(z1)**2,
    'unweighted_mean_active_echo_amplitude': mean_active_amp,
    'unweighted_mean_active_echo_power': mean_active_power,
    'blood_channel_note': 'ENCSR000CUT is peripheral-blood-derived mononuclear cells, not whole blood.',
    'units_note': 'Read-level CPM proxy, not transcript TPM.'
}
(base / 'merged_tp53_echo.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
