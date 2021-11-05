#!/usr/bin/env nextflow

Channel.from(params.output).into {out_ch1; out_ch2}

process docker_test {
    publishDir "$o", mode: 'copy', overwrite: true

    input:
    val o from out_ch1

    output:
    file 'output.txt' into void_ch

    shell:
    '''
    docker version > output.txt
    '''
}

process docker_in_process {
    publishDir "$o", mode: 'copy', overwrite: true

    input:
    val o from out_ch2

    output:
    file 'output.txt' into void_ch2

    script:
    """
    docker_test.py > output.txt
    """
}