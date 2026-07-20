# RawNet2 Evaluation & Benchmarking Suite — Universal Documentation

This document serves as the comprehensive repository and project guide for the robustness benchmarking suite of the **RawNet2** speaker anti-spoofing model under various channel degradations, additive noise, telephony compression codecs, and OOD generalization scenarios.

---

## 1. Directory Structure

```text
d:\RawNet2
├── dataset/                                # Core ASVspoof 2019 dataset components
├── degraded_data/                          # Degraded audio folders for each condition
│   ├── pristine/                           # Baseline clean audio (.wav)
│   ├── codec/                              # Standard codec formats (g711, opus, amr)
│   ├── voip/                               # VoIP degradation (packet loss)
│   ├── noise_0db/ to noise_30db/           # Additive noise categories at various SNRs
│   └── ASVspoof2019.LA.cm.eval_subset.trl.txt # ASVspoof evaluation protocol metadata
├── experiments/                            # Plotting, metrics, and script suite
│   ├── experiment_metrics/                 # Generated outputs directory
│   │   ├── embeddings/                     # High-dimensional embeddings and logits
│   │   │   ├── labels.npy                  # True label file (1 = Genuine, 0 = Spoof)
│   │   │   ├── filenames.txt               # Audio file ID list
│   │   │   ├── pristine_embeddings.npy     # Latent space embeddings (1024D)
│   │   │   └── *_logits.npy                # Evaluated log probabilities
│   │   ├── results/                        # Statistical CSV tables
│   │   │   ├── e1_overall_performance.csv
│   │   │   ├── e2_auc_table.csv
│   │   │   └── ... (20 CSV files)
│   │   └── figures/                        # Academic publication plots
│   │       ├── e1_core_metrics.png
│   │       ├── e2_roc_curves.png
│   │       └── ... (21 PNG files)
│   ├── evaluate_e1.py to evaluate_e20.py   # Individual experiment runners
│   ├── metrics.py                          # Core metric libraries (EER, ECE, FRR/FAR)
│   ├── graph_template_guide.py             # Global styles and templates for plotting
│   └── run_all_evaluations.py              # Master runner to execute E1-E20 end-to-end
├── venv/                                   # Python virtual environment
└── project_documentation.md                # This file
```

---

## 2. Environment Setup & Execution

### Environment Details
- **Python Version**: Python 3.13 (Windows Store Package)
- **Virtual Environment Path**: [d:\RawNet2\venv\Scripts\python.exe](file:///d:/RawNet2/venv/Scripts/python.exe)
- **Core Dependencies**: `numpy`, `pandas`, `matplotlib`, `seaborn`, `scikit-learn`, `scipy`, `soundfile`

### Execution Guides

To run the entire benchmarking pipeline and regenerate all figures/results:
```powershell
# Navigate to the workspace and run the master script
cd d:\RawNet2
.\venv\Scripts\python.exe experiments/run_all_evaluations.py
```

To run a specific evaluation script (e.g., E10):
```powershell
.\venv\Scripts\python.exe experiments/evaluate_e10.py
```

---

## 3. Experiments & Results Summary

### Core Performance Metrics (E1)
- **Goal:** Assess accuracy, precision, recall, F1-score, AUC, and EER under baseline degradations.
- **Output:** [e1_core_metrics.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e1_core_metrics.png) (Grouped Bar Chart)
- **CSV Summary:** [e1_overall_performance.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e1_overall_performance.csv)

| Condition | Accuracy (%) | EER (%) | F1-Score (%) |
|:---|---:|---:|---:|
| **Pristine** | 95.56 | 4.36 | 95.68 |
| **G.711 μ-law** | 95.56 | 4.36 | 95.68 |
| **VoIP** | 87.03 | 5.69 | 85.32 |
| **Ambient Noise (30dB)** | 95.23 | 4.26 | 95.36 |
| **Ambient Noise (20dB)** | 94.46 | 4.46 | 94.70 |

---

### Noise SNR Sweep (E7)
- **Goal:** Sweep ambient noise levels from SNR 30dB down to 0dB to locate the model's breakdown limits.
- **Output:** [e7_noise_snr_sweep.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e7_noise_snr_sweep.png) (Dual-Axis Sweep)
- **CSV Summary:** [e7_snr_table.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e7_snr_table.csv)

| SNR (dB) | Accuracy (%) | EER (%) |
|---:|---:|---:|
| **30** | 95.23 | 4.26 |
| **20** | 94.46 | 4.46 |
| **15** | 92.82 | 5.23 |
| **10** | 88.44 | 6.67 |
| **5** | 79.72 | 9.69 |
| **0** | 62.92 | 22.00 |

---

### Telephony Codec Sweeps (E8 & E9)
- **Goal:** Evaluate detector performance against compression codecs (G.711, G.722, AMR, Opus).
- **Output:** [e8_codec_sweep.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e8_codec_sweep.png) and [e9_opus_bitrate_sweep.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e9_opus_bitrate_sweep.png)
- **CSV Summaries:** [e8_codec_table.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e8_codec_table.csv) and [e9_bitrate_table.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e9_bitrate_table.csv)

| Codec / Bitrate | Accuracy (%) | EER (%) |
|:---|---:|---:|
| **Opus 12k** | 95.03 | 4.15 |
| **G.711 A-law** | 95.56 | 4.36 |
| **G.722** | 95.56 | 4.36 |
| **AMR-WB** | 95.56 | 4.36 |
| **AMR-NB** | 74.41 | 7.33 |
| **Opus 6k** | 68.05 | 8.51 |

---

### AASIST vs. RawNet2 Model Comparison (E10)
- **Goal:** Direct side-by-side performance contrast of AASIST (SOTA) vs. RawNet2 (Baseline) across conditions.
- **Output:** [e10_model_comparison.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e10_model_comparison.png) (1x2 Subplots)
- **CSV Summary:** [e10_detector_comparison.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e10_detector_comparison.csv)

| Condition | AASIST Acc (%) | RawNet2 Acc (%) | AASIST EER (%) | RawNet2 EER (%) |
|:---|---:|---:|---:|---:|
| **Pristine** | 99.26 | 95.56 | 0.72 | 4.36 |
| **G.711 μ-law** | 99.10 | 95.56 | 0.87 | 4.36 |
| **VoIP** | 96.33 | 87.03 | 3.69 | 5.69 |
| **Ambient Noise (20dB)** | 98.33 | 94.46 | 1.64 | 4.46 |

---

### OOD Generalization Heatmap (E11)
- **Goal:** Evaluate out-of-distribution generalization accuracy under a Pristine-tuned threshold.
- **Output:** [e11_generalization_heatmap.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e11_generalization_heatmap.png) (1x18 horizontal RdYlGn heatmap)
- **CSV Summary:** [e11_cross_condition.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e11_cross_condition.csv)

---

### Failure Mode Breakdown (E12)
- **Goal:** Separate errors into False Alarms (Genuine -> Spoof) and False Rejections (Spoof -> Genuine).
- **Output:** [e12_failure_modes.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e12_failure_modes.png) (Stacked Bar Chart)
- **CSV Summary:** [e12_failure_cases.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e12_failure_cases.csv)

---

### Calibration & Calibration Gap (E14)
- **Goal:** Measure model probability calibration and reliability.
- **Output:** [e14_reliability_diagrams.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e14_reliability_diagrams.png) (Reliability diagram with ECE gap shading)
- **CSV Summary:** [e14_calibration_metrics.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e14_calibration_metrics.csv)

---

### Statistical Significance (E15)
- **Goal:** Compute McNemar exact tests and bootstrap 95% confidence intervals relative to Pristine.
- **Output:** [e15_significance_charts.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e15_significance_charts.png) (CI error bars with significance asterisks)
- **CSV Summary:** [e15_significance_table.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e15_significance_table.csv)

---

### Latent Space t-SNE & PCA (E19)
- **Goal:** Map the high-dimensional latent space representations to 2D projections.
- **Outputs:**
  - [e19_tsne_pristine.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e19_tsne_pristine.png) (2D t-SNE scatter)
  - [e19_tsne_voip.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e19_tsne_voip.png) (2D t-SNE scatter)
  - [e19_pca_grid.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e19_pca_grid.png) (2x2 PCA Projection Grid)
- **CSV Summary:** [e19_embedding_observations.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e19_embedding_observations.csv)

---

### Deployment Readiness (E20)
- **Goal:** Dynamic deployment ranking and verdicts based on model vulnerabilities.
- **CSV Summary:** [e20_deployment_summary.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e20_deployment_summary.csv)

| Channel Condition | EER (%) | Readiness Verdict | Recommendation |
|:---|---:|:---|:---|
| **Opus 12k** | 4.15 | Ready | Deployable immediately. |
| **G.711 μ-law** | 4.36 | Ready | Deployable immediately. |
| **Ambient Noise (20dB)** | 4.46 | Ready | Deployable immediately. |
| **VoIP (5% Packet Loss)** | 5.69 | Conditional | Requires front-end speech enhancement. |
| **Ambient Noise (10dB)** | 6.67 | Conditional | Requires front-end speech enhancement. |
| **Opus 6k** | 8.51 | Conditional | Requires front-end speech enhancement. |
| **Ambient Noise (0dB)** | 22.00 | Needs Improvement | High vulnerability to spoofing; must retrain. |

---

## 4. Master Outputs Checklist

All generated results and figures are strictly saved inside the `experiments/experiment_metrics/` directory.

### CSV Tables (results/)
1. [e1_overall_performance.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e1_overall_performance.csv)
2. [e2_auc_table.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e2_auc_table.csv)
3. [e3_ap_table.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e3_ap_table.csv)
4. [e4_confusion_counts.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e4_confusion_counts.csv)
5. [e5_threshold_table.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e5_threshold_table.csv)
6. [e6_delta_metrics.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e6_delta_metrics.csv)
7. [e7_snr_table.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e7_snr_table.csv)
8. [e8_codec_table.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e8_codec_table.csv)
9. [e9_bitrate_table.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e9_bitrate_table.csv)
10. [e10_detector_comparison.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e10_detector_comparison.csv)
11. [e11_cross_condition.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e11_cross_condition.csv)
12. [e12_failure_cases.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e12_failure_cases.csv)
13. [e13_score_means.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e13_score_means.csv)
14. [e14_calibration_metrics.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e14_calibration_metrics.csv)
15. [e15_significance_table.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e15_significance_table.csv)
16. [e16_runtime_table.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e16_runtime_table.csv)
17. [e17_memory_table.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e17_memory_table.csv)
18. [e19_embedding_observations.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e19_embedding_observations.csv)
19. [e20_deployment_summary.csv](file:///d:/RawNet2/experiments/experiment_metrics/results/e20_deployment_summary.csv)

### PNG Figures (figures/)
1. [e1_core_metrics.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e1_core_metrics.png)
2. [e2_roc_curves.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e2_roc_curves.png)
3. [e3_pr_curves.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e3_pr_curves.png)
4. [e4_confusion_grid.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e4_confusion_grid.png)
5. [e5_threshold_vs_acc.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e5_threshold_vs_acc.png)
6. [e6_metrics_trend.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e6_metrics_trend.png)
7. [e7_noise_snr_sweep.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e7_noise_snr_sweep.png)
8. [e8_codec_sweep.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e8_codec_sweep.png)
9. [e9_opus_bitrate_sweep.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e9_opus_bitrate_sweep.png)
10. [e10_model_comparison.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e10_model_comparison.png)
11. [e11_generalization_heatmap.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e11_generalization_heatmap.png)
12. [e12_failure_modes.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e12_failure_modes.png)
13. [e13_score_distributions.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e13_score_distributions.png)
14. [e14_reliability_diagrams.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e14_reliability_diagrams.png)
15. [e15_significance_charts.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e15_significance_charts.png)
16. [e16_runtime_chart.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e16_runtime_chart.png)
17. [e17_memory_chart.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e17_memory_chart.png)
18. [e18_spectrogram_distortions.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e18_spectrogram_distortions.png)
19. [e19_pca_grid.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e19_pca_grid.png)
20. [e19_tsne_pristine.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e19_tsne_pristine.png)
21. [e19_tsne_voip.png](file:///d:/RawNet2/experiments/experiment_metrics/figures/e19_tsne_voip.png)
