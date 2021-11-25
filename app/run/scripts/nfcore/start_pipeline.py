from django.conf import settings
from ..tasks import run_pipe

import logging
import os

logger = logging.getLogger(__name__)


def atacseq(script_location, design_file, single_end, igenome_reference, fasta_file, gtf_annotation,
            macs_size, narrow_peaks):
    print("Starting nextflow pipeline...")
    command = ['nextflow', 'run',
               # '%s' % script_location,
               'nf-core/atacseq',
               # '-profile', 'conda',
               '--input', '%s' % design_file, '--max_memory', '8.GB', '--max_cpus', '8'
               #  , '--outdir', '%s' % outdir,
               ]
    if single_end == 'true':
        command.extend(['--single_end', 'True'])
    else:
        pass
    if igenome_reference is not None:
        command.extend(['--genome', '%s' % igenome_reference])
    if fasta_file != "None":
        command.extend(['--fasta', '%s' % fasta_file])
    if gtf_annotation != "None":
        command.extend(['--gtf', gtf_annotation])
    if macs_size is not None:
        command.extend(['--macs_gsize', '%s' % macs_size])
    if narrow_peaks:
        command.extend(['--narrow_peak', 'True'])

    print("atacseq-command:", command)
    start_msg = "Starting ATAC-seq pipeline..."
    stop_msg = "ATAC-Seq pipeline finished successfully!"

    m_env = os.environ.copy()
    m_env["PATH"] = m_env["PATH"] + ":/root/miniconda3/envs/nf-core-atacseq-1.2.1-chipseq-1.2.2/bin:" \
                                    ":/root/miniconda3/envs/nf-core-rnaseq-3.4/bin"

    print("PATH: ", m_env["PATH"])

    result = run_pipe(command=command, start_msg=start_msg, stop_msg=stop_msg, m_env=m_env)
    result = {'exit': result, 'command': ' '.join(command)}
    return result


def rnaseq(
        csv_file, umi_value, umi_method, umi_pattern, igenome_reference, fasta_file, gtf_file,
        # gff_file,
        bed_file, transcript_fasta, star_index_name, hisat2_index_name, rsem_index_name, salmon_index_name, aligner,
        pseudo_salmon_value
):
    scirpt_location = str(settings.BASE_DIR) + "/nfscripts/nfcore/rnaseq/main.nf"

    command = ['nextflow', 'run',
               # '%s' % scirpt_location,
               'nf-core/rnaseq',
               '-r', '3.3',
               # '-r', '3.4',
               '--input', '%s' % csv_file, '--max_memory', '8.GB', '--max_cpus', '8']
    if umi_value is True:
        command.extend(['--with_umi', 'True', '--umitools_extract_method', '%s' % umi_method, '--umitools_bc_pattern',
                        '%s' % umi_pattern])
    else:
        pass
    if igenome_reference is not None:
        command.extend(['--genome', '%s' % igenome_reference])
    if fasta_file is not None:
        command.extend(['--fasta', '%s' % fasta_file])
    if gtf_file is not None:
        command.extend(['--gtf', '%s' % gtf_file])
    if bed_file is not None:
        command.extend(['--gene_bed', '%s' % bed_file])
    if transcript_fasta is not None:
        command.extend(['--transcript_fasta', '%s' % transcript_fasta])
    if star_index_name is not None:
        command.extend(['--star_index', '%s' % star_index_name])
    if hisat2_index_name is not None:
        command.extend(['--hisat2_index', '%s' % hisat2_index_name])
    if rsem_index_name is not None:
        command.extend(['--rsem_index', '%s' % rsem_index_name])
    if salmon_index_name is not None:
        command.extend(['--salmon_index', './%s' % salmon_index_name])
    if aligner is not None:
        command.extend(['--aligner', '%s' % aligner])
    if pseudo_salmon_value:
        command.extend(['--pseudo_aligner', 'salmon'])

    print("rnaseq-command:", command)

    start_msg = "Starting RNA-Seq Pipeline.."
    stop_msg = "RNA-Seq Pipeline finished successfully!"

    m_env = os.environ.copy()
    m_env["PATH"] = m_env["PATH"] + ":/root/miniconda3/envs/nf-core-rnaseq-3.4/bin" \
                                    ":/root/miniconda3/envs/nf-core-atacseq-1.2.1-chipseq-1.2.2/bin"

    print("PATH: ", m_env["PATH"])

    result = run_pipe(command=command, start_msg=start_msg, stop_msg=stop_msg, m_env=m_env)
    result = {'exit': result, 'command': ' '.join(command)}
    return result


def chipseq(design_file, single_end, igenome_reference, fasta_file, gtf_file, bed_file, macs_size, narrow_peaks):
    script_location = str(settings.BASE_DIR) + "/nfscripts/nfcore/chipseq/main.nf"
    # script_location = str(settings.BASE_DIR) + "/nfscripts/nfcore/chipseq/main_loc.nf"
    command = [
        'nextflow', 'run',
        # 'nf-core/chipseq',
        '%s' % script_location,
        # '-profile', 'docker',
        # '-profile', 'conda',
        '--input', '%s' % design_file
    ]
    if single_end is True:
        command.extend(['--single_end', 'True'])
    if igenome_reference is not None:
        command.extend(['--genome', '%s' % igenome_reference])
    if fasta_file is not None:
        command.extend(['--fasta', '%s' % fasta_file])
    if gtf_file is not None:
        command.extend(['--gtf', '%s' % gtf_file])
    if bed_file is not None:
        command.extend(['--gene_bed', '%s' % bed_file])
    if macs_size is not None:
        command.extend(['--macs_gsize', '%s' % macs_size])
    if narrow_peaks:
        command.extend(['--narrow_peak', 'True'])

    command.extend(['--max_memory', '8.GB', '--max_cpus', '8'])

    print("chipseq-command:", command)

    start_msg = "Starting ChIP-Seq pipeline.."
    stop_msg = "ChIP-Seq pipeline finished successfully!"
    m_env = os.environ.copy()
    m_env["PATH"] = m_env["PATH"] + ":/root/miniconda3/envs/nf-core-atacseq-1.2.1-chipseq-1.2.2/bin:"\
                                    ":/root/miniconda3/envs/nf-core-rnaseq-3.4/bin"

    print("PATH: ", m_env["PATH"])

    result = run_pipe(command=command, start_msg=start_msg, stop_msg=stop_msg, m_env=m_env)
    result = {'exit': result, 'command': ' '.join(command)}
    return result


def sarek(tsv_file, igenome_reference, fasta_file, dbsnp, dbsnp_index, tools):
    script_location = str(settings.BASE_DIR) + "/nfscripts/nfcore/sarek/main.nf"
    command = ['nextflow', 'run',
               '%s' % script_location,
               # 'nf-core/sarek',
               '--input', '%s' % tsv_file, '--max_memory', '8.GB', '--max_cpus', '8'
               # , '--skip_qc', 'bamqc,BaseRecalibrator'
               ]
    if igenome_reference is not None:
        command.extend(['--genome', '%s' % igenome_reference])
    if dbsnp is not None:
        if dbsnp_index is not None:
            command.extend(['--dbsnp', '%s' % dbsnp, '--dbsnp_index', '%s' % dbsnp_index])
    else:
        command.extend(['--skip_qc', 'BaseRecalibrator'])
    if fasta_file is not None:
        command.extend(['--fasta', '%s' % fasta_file])
    if tools != "":
        command.extend(['--tools', f'{tools}'])
    print("sarek-command:", command)

    # set start_msg, stop_msg and run pipeline
    start_msg = "Starting Sarek pipeline..."
    stop_msg = "Sarek pipeline finished successfully!"

    m_env = os.environ.copy()
    m_env["PATH"] = "/root/miniconda3/envs/nf-core-sarek-2.7/bin:" + m_env["PATH"]  # + \
    # ":/root/miniconda3/envs/nf-core-atacseq-1.2.1-chipseq-1.2.2/bin" \
    # ":/root/miniconda3/envs/nf-core-rnaseq-3.4/bin"

    print("PATH: ", m_env["PATH"])

    result = run_pipe(command=command, start_msg=start_msg, stop_msg=stop_msg, m_env=m_env)
    result = {'exit': result, 'command': ' '.join(command)}
    return result


def atacseq_advanced(
        run_name, config_file, design_file, single_end, fragment_size, seq_center, email, genome_reference, fasta_file,
        gtf_annotation, bwa_index_name, gene_bed, tss_bed, macs_gsize, blacklist, mito_name, save_reference, clip_r1,
        clip_r2,
        three_prime_clip_r1, three_prime_clip_r2, trim_nextseq, skip_trimming, save_trimmed, keep_mito, keep_dups,
        keep_multi_map,
        bwa_min_score, skip_merge_replicates, save_align_intermeds, narrow_peak, broad_cutoff, macs_fdr, macs_pvalue,
        min_reps_consensus,
        save_macs_pileup, skip_peak_qc, skip_peak_annotation, skip_consensus_peaks, deseq2_vst, skip_diff_analysis,
        skip_fastqc,
        skip_picard_metrics, skip_preseq, skip_plot_profile, skip_plot_fingerprint, skip_ataqv, skip_igv, skip_multiqc
):
    command = [
        'nextflow', 'run', 'nf-core/atacseq',
        '--max_memory', '8.GB', '--max_cpus', '8'
    ]
    if run_name is not None:
        command.extend(['-name', '%s' % run_name])
    if config_file != "None":
        command.extend(['-profile', '%s' % config_file])
    if design_file != "None":
        command.extend(['--input', '%s' % design_file])
    if single_end:
        command.extend(['--single_end'])
    if fragment_size is not None:
        command.extend(['--fragment_size', '%s' % fragment_size])
    if seq_center is not None:
        command.extend(['--seq_center', '%s' % seq_center])
    if email is not None:
        command.extend(['--email', '%s' % email])
    if genome_reference is not None:
        command.extend(['--genome', '%s' % genome_reference])
    if fasta_file != "None":
        command.extend(['--fasta', '%s' % fasta_file])
    if gtf_annotation != "None":
        command.extend(['--gtf', '%s' % gtf_annotation])
    if bwa_index_name is not None:
        command.extend(['--bwa_index', '%s' % bwa_index_name])
    if gene_bed != "None":
        command.extend(['--gene_bed', '%s' % gene_bed])
    if tss_bed != "None":
        command.extend(['--tss_bed', '%s' % tss_bed])
    if macs_gsize is not None:
        command.extend(['--macs_gsize', '%s' % macs_gsize])
    if blacklist != "None":
        command.extend(['--blacklist', '%s' % blacklist])
    if mito_name is not None:
        command.extend(['--mito_name', '%s' % mito_name])
    if save_reference:
        command.extend(['--save_reference'])
    if clip_r1 is not None:
        command.extend(['--clip_r1', '%s' % clip_r1])
    if clip_r2 is not None:
        command.extend(['--clip_r2', '%s' % clip_r2])
    if three_prime_clip_r1 is not None:
        command.extend(['--three_prime_clip_r1', '%s' % three_prime_clip_r1])
    if three_prime_clip_r2 is not None:
        command.extend(['--three_prime_clip_r2', '%s' % three_prime_clip_r2])
    if trim_nextseq is not None:
        command.extend(['--trim_nextseq', '%s' % trim_nextseq])
    if skip_trimming:
        command.extend(['--skip_trimming'])
    if save_trimmed:
        command.extend(['--save_trimmed'])
    if keep_mito:
        command.extend(['--keep_mito'])
    if keep_dups:
        command.extend(['--keep_dups'])
    if keep_multi_map:
        command.extend(['--keep_multi_map'])
    if bwa_min_score is not None:
        command.extend(['--bwa_min_score', '%s' % bwa_min_score])
    if skip_merge_replicates:
        command.extend(['--skip_merge_replicates'])
    if save_align_intermeds:
        command.extend(['--save_align_intermeds'])
    if narrow_peak:
        command.extend(['--narrow_peak'])
    if broad_cutoff is not None:
        command.extend(['--broad_cutoff', '%s' % broad_cutoff])
    if macs_fdr is not None:
        command.extend(['--macs_fdr', '%s' % macs_fdr])
    if macs_pvalue is not None:
        command.extend(['--macs_pvalue', '%s' % macs_pvalue])
    if min_reps_consensus is not None:
        command.extend(['--min_reps_consensus', '%s' % min_reps_consensus])
    if save_macs_pileup:
        command.extend(['--save_macs_pileup'])
    if skip_peak_qc:
        command.extend(['--skip_peak_qc'])
    if skip_peak_annotation:
        command.extend(['--skip_peak_annotation'])
    if skip_consensus_peaks:
        command.extend(['--skip_consensus_peaks'])
    if deseq2_vst:
        command.extend(['--deseq2_vst'])
    if skip_diff_analysis:
        command.extend(['--skip_diff_analysis'])
    if skip_fastqc:
        command.extend(['--skip_fastqc'])
    if skip_picard_metrics:
        command.extend(['--skip_picard_metric'])
    if skip_preseq:
        command.extend(['--skip_preseq'])
    if skip_plot_profile:
        command.extend(['--skip_plot_profile'])
    if skip_plot_fingerprint:
        command.extend(['--skip_plot_fingerprint'])
    if skip_ataqv:
        command.extend(['--skip_ataqv'])
    if skip_igv:
        command.extend(['--skip_igv'])
    if skip_multiqc:
        command.extend(['--skip_multiqc'])

    # print command
    print("advanced atacseq command:", command)

    # set start_msg, stop_msg and run pipeline
    start_msg = "Starting advanced ATAC-Seq pipeline..."
    stop_msg = "Pipeline finished successfully!"
    result = run_pipe(command=command, start_msg=start_msg, stop_msg=stop_msg)
    return result
