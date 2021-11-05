#!/usr/bin/env nextflow

//params.str

mediaroot_ch = Channel.fromPath(params.mediaroot)
zip_ch = Channel.fromPath(params.species)

process ZipToMediaroot {
	publishDir "$mr", mode: 'copy', overwrite: true

	input:
	val mr from mediaroot_ch
	file zipspecies from zip_ch

	output:
	file 'report.zip' into void_ch

	shell:
	'''
	zip report.zip !{mr}/!{zipspecies}
	cp ./report.zip !{mr}
	'''

}
