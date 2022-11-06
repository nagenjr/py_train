from jinja2 import Template
import yaml
import sys
import os
from glob import glob
import copy

def versiontuple(v):
    return tuple(map(int, (v.split("."))))

def yamlload(input):
    if versiontuple(yaml.__version__) < (5,1):
        return yaml.load(input)
    else:
        return yaml.load (input, Loader = yaml.FullLoader)

if sys.version_info <= (3,0):
    reload(sys)
    sys.setdefaultencoding('utf8')

def dst_path_name(yml_file, routername = None):
    parent_path, filename = os.path.split(yml_file)
    if routername:
        if parent_path != '':
            dst_path = parent_path + '/' + routername
        else:
            dst_path = routername
    else:
        tail_length = len(yml_file.split('.')[-1])
        if tail_length < len(yml_file):
            routername = filename[0:-(tail_length + 1)]
            dst_path = yml_file[0:-(tail_length + 1)]
        else:
            routername = filename
            dst_path = yml_file + '_CFG'
        #dst_path = yml_file[0:len(yml_file)-4]
        #routername = filename[0:-len('.yml')]

    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    return parent_path, dst_path, routername

def build_single_yml(dict_data, loc ):
    if isinstance(dict_data,dict):
        for k in list(dict_data):
            v = dict_data[k]
        #for k,v in dict_data.items():
            if isinstance(v, list):
                if isinstance(v[0], dict):
                    for list_item in v:
                        build_single_yml(list_item, loc)

                    while {} in v:
                        v.remove({})
                    if len(v) == 0:
                        dict_data.pop(k, None)
                else:
                    if len(v) > loc and v[loc] != '':
                        dict_data[k] = v[loc]
                    else:
                        dict_data.pop(k, None)
            elif isinstance(v, dict):
                build_single_yml(v, loc)
                if not bool(v):
                    dict_data.pop(k)


def merge(user, default):
    if isinstance(user,dict) and isinstance(default,dict):
        #for k,v in default.iteritems():
        for k,v in default.items():
            if k not in user:
                user[k] = v
            else:
                user[k] = merge(user[k],v)
    elif isinstance(user,list) and isinstance(default,list):
        user += default
    return user

def render_dict(datavars, template_fname, foldername, total_file = None):

    template = Template(open(template_fname).read())
    sout = template.render(datavars)
    if sout != '' and sout !='\n':
        OutPut= foldername + template_fname[len('templates') : len(template_fname)-len('.j2')] + '.txt'
        ofile = open(OutPut,"w")
        ofile.write(sout)
        ofile.close()
        if total_file and '01_mgmt_init_setup' not in template_fname:
            total_file.write(sout)
        print (sout)

def rever_render(datavars, parent_path, routername, expansion = '.yaml'):

    abspath = os.path.abspath(__file__)
    items = abspath.split(os.sep)

    if len(items) >= 2:
        prender_dir = os.path.expanduser('~') + '/' + items[-1][0:-len('.py')] + '_LOG'
        if not os.path.exists(prender_dir):
            os.makedirs(prender_dir)
        code_dir = prender_dir + '/' + items[-2]
        if not os.path.exists(code_dir):
            os.makedirs(code_dir)

        dst_file = code_dir + '/' + routername + expansion
    else:
        if parent_path != '':
            dst_file = parent_path + '/' + routername + expansion
        else:
            dst_file = routername + expansion

    ## Too difficult to keep update with all files, just build in function to do it
    ## Althoug it doesn't look very well, but it is just for debug
    with open(dst_file, 'w') as outfile:
        yaml.dump(datavars, outfile, default_flow_style=False)
        #template = Template(open('config.j2').read())
        #ofile = open(dst_file,"w")
        #sout = template.render(datavars)
        #ofile.write(sout)
        #ofile.close()

def find_common_file(parent_path):
    if os.path.isfile(parent_path + '/common.yml'):
        return parent_path + '/common.yml'
    path, filename = os.path.split(parent_path)
    while path != '/' and path != '':
        if os.path.isfile(path + '/common.yml'):
            return path + '/common.yml'
        else:
            path, filename = os.path.split(path)
    if os.path.isfile('common.yml'):
        return 'common.yml'
    return None

def merge_dict(datavars, parent_path):
    common_file = find_common_file(parent_path)
    if common_file is not None:
        commonvars = yamlload(open(common_file).read())
        datavars = merge(datavars, commonvars)
    return datavars

def render(datavars, yml_file, template_fname = None, routername = None):

    parent_path, dst_path, router = dst_path_name(yml_file, routername)

    if routername:
        rever_render(datavars, parent_path, router)

    merge_dict(datavars, parent_path)
    rever_render(datavars, parent_path, router, '_full.yaml')
    total_file = open(dst_path + '/' + router + '_cfg.txt',"w")

    if template_fname is not None:
        #OutPut=dst_path + template_fname[len('templates') :len(template_fname)-len('.j2')] + '.txt'
        render_dict(datavars, template_fname, dst_path, total_file)
    else:
        template_fname = sorted(glob('templates/*.j2'))

        for t_fname in template_fname:
            #OutPut=dst_path + t_fname[len('templates')  : len(t_fname)-len('.j2')] + '.txt'
            render_dict(datavars, t_fname, dst_path, total_file)

    total_file.close()


def generate_cfg(yml_file, template = None):

    datavars = yamlload(open(yml_file).read())

    if "MANAGEMENT" in datavars.keys() and "HOSTNAME" in datavars["MANAGEMENT"] and isinstance( datavars["MANAGEMENT"]["HOSTNAME"], list):
        for host in datavars["MANAGEMENT"]["HOSTNAME"]:
            single_yml = copy.deepcopy(datavars)
            build_single_yml(single_yml, datavars["MANAGEMENT"]["HOSTNAME"].index(host))

            render(single_yml,yml_file, template_fname = template, routername = host)
    else:
        if "MANAGEMENT" in datavars.keys() and "HOSTNAME" in datavars["MANAGEMENT"]:
            render(datavars,yml_file, template_fname = template,  routername = datavars["MANAGEMENT"]["HOSTNAME"])
        else:
            render(datavars,yml_file, template_fname = template )


datavars_fname = './'
if len(sys.argv) >1:
    datavars_fname = sys.argv[1]

if not os.path.exists(datavars_fname):
    print('Please provide the valid YAML files locations')
    sys.exit()

template_fname = None
if len(sys.argv) == 3:
    template_fname = sys.argv[2]
    if not os.path.isfile(template_fname):
        print('Template file not exist')
        sys.exit()

if os.path.isfile(datavars_fname):
    generate_cfg(datavars_fname, template_fname)
else:
    for root, dirs, files in os.walk(datavars_fname):
        for name in files:
            if (name[-len('.yml'):]  == '.yml') and ('common.yml' not in name):
                #print(os.path.join(root, name))
                generate_cfg(os.path.join(root, name), template_fname)

