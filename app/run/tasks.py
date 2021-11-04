import shutil
from random import choice
from string import ascii_uppercase, ascii_lowercase, digits
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import os
import subprocess as sp
import tarfile


def store(run_id, file):
    media_path = get_media_path(run_id)
    fs = FileSystemStorage(location=media_path, base_url=settings.MEDIA_URL + 'run/' + run_id + '/')
    filename = fs.save(file.name, file)
    file_url = fs.url(filename)
    return file_url


def random_string_id(x):
    string = (''.join(choice(ascii_lowercase + ascii_uppercase + digits) for i in range(x)))
    return string


def generate_and_check_id():
    run_id = random_string_id(16)
    if os.path.isdir(str(settings.MEDIA_ROOT) + '/run/' + run_id):
        generate_and_check_id()
    else:
        return run_id


def generate_and_check_sheet_id():
    sheet_id = random_string_id(16)
    if os.path.isdir(str(settings.MEDIA_ROOT) + '/spreadsheets/' + sheet_id):
        generate_and_check_id()
    else:
        return sheet_id


def get_id_path(run_id):
    id_path = str(settings.BASE_DIR) + "/media/run/" + run_id + "/"
    print("id_path: ", id_path)
    return id_path


def get_media_path(run_id):
    media_path = str(settings.MEDIA_ROOT) + "/run/" + run_id + "/"
    print("media_path: ", media_path)
    return media_path


def create_directory(directory):
    if not os.path.exists(directory):
        Path(directory).mkdir(parents=True, exist_ok=False)
    return 0


def create_progress_file(directory):
    open('%s/.inprogress.txt' % directory, 'a').close()


def create_crash_file(directory, error):
    with open('%s/.crashed.txt' % directory, 'w') as fl:
        print("%s" % error, file=fl)


def create_completion_file(directory):
    open("%s/.completed.txt" % directory, "a").close()


def get_upload_path(run_id):
    upload_path = settings.MEDIA_ROOT + '/run/{run_id}/'.format(run_id=run_id)
    return upload_path


def handle_uploaded_file(f, run_id):
    with open(settings.MEDIA_ROOT + '/run/' + run_id + '/' + f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return 0


def handle_and_unzip(z, run_id):
    with open(settings.MEDIA_ROOT + '/run/' + run_id + '/' + z.name, "wb+") as destination:
        for chunk in z.chunks():
            destination.write(chunk)
    path = settings.MEDIA_ROOT + '/run/' + run_id + '/'
    file = path + z.name
    # print('path: ', path)
    # print('file: ', file)
    command = ['unzip', '-o', file, '-d', path]
    process = sp.run(command,
                     stdout=sp.PIPE,
                     stderr=sp.PIPE,
                     shell=False,
                     universal_newlines=True
                     )
    print(process.returncode)
    return 0


def handle_and_untar(t, run_id):
    path = settings.MEDIA_ROOT + '/run/' + run_id + '/'
    with open(path + t.name, "wb+") as destination:
        for chunk in t.chunks():
            destination.write(chunk)
    file = path + t.name
    print(file)
    command = ['tar', '-xvzf', '%s' % file, '-C', '%s' % path, '--no-same-owner']
    process = sp.run(command,
                     stdout=sp.PIPE,
                     stderr=sp.PIPE,
                     shell=False,
                     universal_newlines=True)
    print("untar stdout: ", process.stdout)
    print("untar stderr: ", process.stderr)
    print("untar returncode: ", process.returncode)
    return 0


def handle_uploaded_zip(z, run_id):
    with open(settings.MEDIA_ROOT + '/run/' + run_id + '/' + z.name, "wb+") as destination:
        for chunk in z.chunks():
            destination.write(chunk)
    return 0


def unzip_file(z, run_id):
    path = settings.MEDIA_ROOT + '/run/' + run_id + '/'
    file = path + z.name
    print(file)
    command = ['unzip', '-o', file, '-d', path]
    process = sp.run(command,
                     stdout=sp.PIPE,
                     stderr=sp.PIPE,
                     shell=False,
                     universal_newlines=True
                     )
    if process.returncode == 0:
        print("unzip finished")
    return 0


def zip_file(name, target, target_2=""):
    command = ['zip', '-r', name, target]
    if target_2 != "":
        command.extend([target_2])
    process = sp.run(command,
                     stdout=sp.PIPE,
                     stderr=sp.PIPE,
                     shell=False,
                     universal_newlines=True
                     )
    if process.returncode == 0:
        print("zip archive finished..")
    return 0


def untar_file(t, run_id):
    path = settings.MEDIA_ROOT + '/run/' + run_id + '/'
    file = path + t.name
    command = ['tar', '-xvzf', '%s' % file, '-C', '%s' % path, '--no-same-owner']
    process = sp.run(command,
                     stdout=sp.PIPE,
                     stderr=sp.PIPE,
                     shell=False,
                     universal_newlines=True)
    print("untar stdout: ", process.stdout)
    print("untar stderr: ", process.stderr)
    if process.returncode != 0:
        import sys
        print("something went wrong")
        sys.exit(process.returncode)
    else:
        print("untar extraction completed")
        return 0


def tar_file(name, target, target_2=""):
    command = ['tar', '-czvf', name, target]
    if target_2 != "":
        command.extend([target_2])
    process = sp.run(command,
                     stdout=sp.PIPE,
                     stderr=sp.PIPE,
                     shell=False,
                     universal_newlines=True
                     )
    if process.returncode == 0:
        print("tar archive finished..")
    return 0


def find_pipeline(pipeline_name, run_id):
    if pipeline_name == 'Post-RNA-Seq':
        # return redirect('run:PRSRun', run_id)
        return redirect('run:PRSRun')

    elif pipeline_name in ['Post-ATAC-Seq', 'Post-ChIP-Seq']:
        # return redirect('run:PACSRun', run_id)
        return redirect('run:PACSRun')
    elif pipeline_name == 'ATAC-Seq':
        # return redirect('run:AtacseqRun', run_id)
        return redirect('run:AtacseqRun')
    elif pipeline_name == 'ChIP-Seq':
        # return redirect('run:ChipseqRun', run_id)
        return redirect('run:ChipseqRun')
    elif pipeline_name == 'RNA-Seq':
        # return redirect('run:RnaseqRun', run_id)
        return redirect('run:RnaseqRun')
    elif pipeline_name == 'Sarek':
        # return redirect('run:SarekRun', run_id)
        return redirect('run:SarekRun')


def start_docker():
    command = ['systemctl', 'start', 'docker']
    process = sp.run(command,
                     stderr=sp.PIPE,
                     stdout=sp.PIPE,
                     shell=False,
                     universal_newlines=True)
    if process.returncode == 0:
        print("Pipeline finished successfully!")
    else:
        print("Pipeline finished with error code:{0}".format(str(process.returncode)))


def cp_file(file_path, target):
    command = ['cp -r %s' % file_path, '%s' % target]
    print("copycommand: ", command)
    from .scripts.tasks import run_pipe
    run_pipe(command=command, start_msg="moving file...", stop_msg="done")


def cp_file_no_r(file_path, target):
    command = ['cp %s' % file_path, '%s' % target]
    print("copycommand: ", command)
    from .scripts.tasks import run_pipe
    run_pipe(command=command, start_msg="moving file...", stop_msg="done")


def mv_file(file_path, target):
    command = ['mv', '%s' % file_path, '%s' % target]
    print("movecommand: ", command)
    from .scripts.tasks import run_pipe
    run_pipe(command=command, start_msg="moving file...", stop_msg="done")


def get_genes_bed(run_id):
    os.getcwd()
    target = settings.MEDIA_ROOT + '/run/' + run_id + '/results/genome/gene_bed_name.txt'
    # target = '/genome/gene_bed_name.txt'

    with open(target, "r") as file:
        gene_bed = file.readline().strip()

    if os.path.exists(settings.MEDIA_ROOT + '/run/' + run_id + '/results/genome/' + gene_bed):
        print("ping ping ping")
    # copy_file(file_path=settings.MEDIA_ROOT + '/run/' + run_id + '/results/genome/' + gene_bed,
    #           target=settings.MEDIA_ROOT + '/run/' + run_id + '/' + gene_bed)

    return gene_bed


def get_gtf(run_id):
    target = settings.MEDIA_ROOT + '/run/' + run_id + '/results/genome/gtf_name.txt'

    with open(target, "r") as file:
        gtf = file.readline().strip()

    if os.path.exists(settings.MEDIA_ROOT + '/run/' + run_id + '/results/genome/' + gtf):
        print("ping ping ping")

    return gtf


def clean_wd():
    keepers = ['report.pdf', 'results.tar.gz', 'results.zip', 'results_post.tar.gz', 'results_post.zip',
               '.nextflow.log', 'keeper.txt', '.completed.txt']
    for filename in os.listdir('.'):
        if filename not in keepers:
            if os.path.isdir(filename):
                print("removing %s" % (filename,))
                shutil.rmtree(filename)
            else:
                print("removing %s" % (filename,))
                os.remove(filename)


def sweep_wd():
    for filename in os.listdir('.'):
        if os.path.isdir(filename):
            print("removing %s" % (filename,))
            shutil.rmtree(filename)
        else:
            print("removing %s" % (filename,))
            os.remove(filename)


def del_file(filelist):
    for filename in os.listdir('.'):
        if filename in filelist:
            if os.path.isdir(filename):
                print("removing %s" % (filename,))
                shutil.rmtree(filename)
            else:
                print("removing %s" % (filename,))
                os.remove(filename)


def rsync_file(
        # target, include, getout
        source, destination, getout, run_id
):
    command = ['rsync', '-avi', source, destination]

    print(command)

    finished = False

    while finished is False:
        process = sp.run(command,
                         stderr=sp.PIPE,
                         stdout=sp.PIPE,
                         shell=False,
                         universal_newlines=True)
        if process.returncode == 0:
            print("File loaded successfully!")
            with open("files.txt", "w") as fl:
                print(process.stdout, file=fl)

            with open("files.txt", "r") as fi:
                for line in fi:
                    items = line.split(" ")
                    print(items)
                    if items[0] == ">f+++++++++":
                        if items[1].strip().endswith(getout):
                            print("item: ", items[1])
                            from distutils.file_util import copy_file
                            target_dir = settings.MEDIA_ROOT + "/run/" + run_id + "/" + items[1].strip()
                            print(target_dir)
                            print("isfile: ", os.path.isfile(target_dir))
                            file_name = items[1].strip().split("/")[1]
                            copy_file(target_dir, settings.MEDIA_ROOT + "/run/" + run_id + "/" + file_name)
                            return file_name.strip()

            finished = True
        else:
            print("File loading with error code:{0}".format(str(process.returncode)))
            print(process.stdout)
            print(process.stderr)
            import time
            time.sleep(5)


def ungzip_file(file):
    print("ungzip-file: ", file)
    return_name = file[:-3]
    print("return_name: ", return_name)
    command = ['gzip', '-d', file]
    print("command: ", command)
    process = sp.run(command,
                     stderr=sp.PIPE,
                     stdout=sp.PIPE,
                     shell=False,
                     universal_newlines=True)
    if process.returncode == 0:
        return return_name
    else:
        print("Unpacking didn't work")
        print(process.stdout)
        print(process.stderr)


def get_taxid(name):
    from ete3 import NCBITaxa
    ncbi = NCBITaxa()
    print("starting name2taxid")
    name2taxid = ncbi.get_name_translator([name])
    tax_value = name2taxid[name]
    species_id = tax_value[0]
    print("species_id", species_id)
    print("finished name2taxid")
    return species_id


def check_for_run_dir(run_id):
    # id_path = settings.MEDIA_ROOT + '/run/' + run_id + '/'
    id_path = get_id_path(run_id)
    print("checking for id_path")
    print(os.path.isdir(id_path))
    if os.path.isdir(id_path):
        print("ping")
        return True
        # return redirect('run:idTaken', run_id)
        # return redirect('run:idTaken', run_id)


########################################################################################################################
# download functions


# download file function
# def download_file(request, run_id, file):
def download_file(request, file_path):
    # get file_path
    # file_path = settings.MEDIA_ROOT + '/run/' + run_id + "/" + file
    filename, file_extension = os.path.splitext(file_path)
    # download file

    if os.path.exists(file_path):
        if file_extension == ".pdf":
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        elif file_extension == ".log":
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="text/plain")
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(
                    file_path)  # give option to download file rather than open in tab
                return response
        elif file_extension == ".tsv":
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="text/tab-separated-values")
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(
                    file_path)  # give option to download file rather than open in tab
                return response
        elif file_extension == ".csv":
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="text/csv")
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(
                    file_path)  # give option to download file rather than open in tab
                return response

    raise Http404


# download zip archive
def download_zip(request, run_id, file):
    # get file_path
    file_path = settings.MEDIA_ROOT + '/run/' + run_id + '/' + file
    # download file
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/zip")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


# download tar archive
def download_tar(request, run_id, file):
    # get file_path
    file_path = settings.MEDIA_ROOT + '/run/' + run_id + '/' + file
    # download file
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/tar.gz")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def download_tutorial(request, pipe, file):
    # get file_path
    file_path = settings.MEDIA_ROOT + '/tutorials/' + pipe + '/' + file
    print('file_path: ', file_path)
    # download file
    if file[-7:] == ".tar.gz":
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/tar.gz")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        else:
            return HttpResponse(
                "It appears this pipeline does not yet have a functioning tutorial-archive.\n" + "We apologize for the inconvenience")
        raise Http404
    elif file[-4:] == ".zip":
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/zip")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        else:
            return HttpResponse(
                "It appears this pipeline does not yet have a functioning tutorial-archive.\n" + "We apologize for the inconvenience")
        raise Http404
