import os
if not os.path.exists("temp"):
    os.mkdir("temp")


def from_io_with_inschek_test():
    import os
    from pyemu import Pst,pst_utils
    # creation functionality
    dir = os.path.join("..","verification","10par_xsec","template_mac")
    pst = Pst(os.path.join(dir,"pest.pst"))


    tpl_files = [os.path.join(dir,f) for f in pst.template_files]
    out_files = [os.path.join(dir,f) for f in pst.output_files]
    ins_files = [os.path.join(dir,f) for f in pst.instruction_files]
    in_files = [os.path.join(dir,f) for f in pst.input_files]


    new_pst = Pst.from_io_files(tpl_files, in_files,
                                ins_files, out_files,
                                pst_filename=os.path.join("temp","test.pst"))
    print(new_pst.observation_data)
    return

def tpl_ins_test():
    import os
    from pyemu import Pst,pst_utils
    # creation functionality
    dir = os.path.join("..","verification","henry","misc")
    files = os.listdir(dir)
    tpl_files,ins_files = [],[]
    for f in files:
        if f.lower().endswith(".tpl") and "coarse" not in f:
            tpl_files.append(os.path.join(dir,f))
        if f.lower().endswith(".ins"):
            ins_files.append(os.path.join(dir,f))

    out_files = [f.replace(".ins",".junk") for f in ins_files]
    in_files = [f.replace(".tpl",".junk") for f in tpl_files]

    pst_utils.pst_from_io_files(tpl_files, in_files,
                                ins_files, out_files,
                                pst_filename=os.path.join("temp","test.pst"))
    return


def res_test():
    import os
    import numpy as np
    from pyemu import Pst,pst_utils
    # residual functionality testing
    pst_dir = os.path.join("pst")

    p = Pst(os.path.join(pst_dir,"pest.pst"))
    phi_comp = p.phi_components
    assert "regul_p" in phi_comp
    assert "regul_m" in phi_comp

    p.adjust_weights_resfile()

    d = np.abs(p.phi - p.nnz_obs)
    assert d < 1.0E-5
    p.adjust_weights(obsgrp_dict={"head": 50})
    assert np.abs(p.phi_components["head"] - 50) < 1.0e-6

    # get()
    new_p = p.get()
    new_p.prior_information = p.prior_information
    new_file = os.path.join("temp", "new.pst")
    new_p.write(new_file)

    p_load = Pst(new_file,resfile=p.resfile)
    for gname in p.phi_components:
        d = np.abs(p.phi_components[gname] - p_load.phi_components[gname])
        assert d < 1.0e-5

def pst_manip_test():
    import os
    from pyemu import Pst
    pst_dir = os.path.join("pst")
    org_path = os.path.join(pst_dir,"pest.pst")
    new_path = os.path.join("temp","pest1.pst")
    pst = Pst(org_path)
    pst.control_data.pestmode = "regularisation"
    pst.write(new_path)
    pst = Pst(new_path)
    pst.svd_data.maxsing = 1
    pst.write(new_path,update_regul=True)


def load_test():
    import os
    from pyemu import Pst,pst_utils
    pst_dir = os.path.join("pst")
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    # just testing all sorts of different pst files
    pst_files = os.listdir(pst_dir)
    exceptions = []
    load_fails = []
    for pst_file in pst_files:
        if pst_file.endswith(".pst"):
            print(pst_file)
            try:
                p = Pst(os.path.join(pst_dir,pst_file))
            except Exception as e:
                exceptions.append(pst_file + " read fail: " + str(e))
                load_fails.append(pst_file)
                continue
            out_name = os.path.join(temp_dir,pst_file)
           #p.write(out_name,update_regul=True)
            try:
                p.write(out_name,update_regul=True)
            except Exception as e:
                exceptions.append(pst_file + " write fail: " + str(e))
                continue
            try:
                p = Pst(out_name)
            except Exception as e:
                exceptions.append(pst_file + " reload fail: " + str(e))
                continue

    #with open("load_fails.txt",'w') as f:
    #    [f.write(pst_file+'\n') for pst_file in load_fails]
    if len(exceptions) > 0:
        raise Exception('\n'.join(exceptions))

def smp_test():
    import os
    from pyemu.pst.pst_utils import smp_to_dataframe,dataframe_to_smp,\
        parse_ins_file,smp_to_ins
    
    smp_filename = os.path.join("misc","gainloss.smp")
    df = smp_to_dataframe(smp_filename)
    print(df.dtypes)
    dataframe_to_smp(df,smp_filename+".test")
    smp_to_ins(smp_filename)
    obs_names = parse_ins_file(smp_filename+".ins")
    print(len(obs_names))

    smp_filename = os.path.join("misc","sim_hds_v6.smp")
    df = smp_to_dataframe(smp_filename)
    print(df.dtypes)
    dataframe_to_smp(df,smp_filename+".test")
    smp_to_ins(smp_filename)
    obs_names = parse_ins_file(smp_filename+".ins")
    print(len(obs_names))


def smp_dateparser_test():
    import os
    from pyemu.pst.pst_utils import smp_to_dataframe,dataframe_to_smp,\
        parse_ins_file,smp_to_ins

    smp_filename = os.path.join("misc","gainloss.smp")
    df = smp_to_dataframe(smp_filename,datetime_format= "%d/%m/%Y %H:%M:%S")
    print(df.dtypes)
    dataframe_to_smp(df,smp_filename+".test")
    smp_to_ins(smp_filename)
    obs_names = parse_ins_file(smp_filename+".ins")
    print(len(obs_names))

    smp_filename = os.path.join("misc","sim_hds_v6.smp")
    df = smp_to_dataframe(smp_filename)
    print(df.dtypes)
    dataframe_to_smp(df,smp_filename+".test")
    smp_to_ins(smp_filename)
    obs_names = parse_ins_file(smp_filename+".ins")
    print(len(obs_names))


def tied_test():
    import os
    import pyemu
    pst_dir = os.path.join("pst")
    pst = pyemu.Pst(os.path.join(pst_dir,"br_opt_no_zero_weighted.pst"))
    print(pst.tied_lines)
    pst.write(os.path.join("temp","pest_tied_tester_1.pst"))
    mc = pyemu.MonteCarlo(pst=pst)
    mc.draw(1)
    mc.write_psts(os.path.join("temp","tiedtest_"))

def derivative_increment_tests():
    import os
    import pyemu

    pst = pyemu.Pst(os.path.join("pst","inctest.pst"))
    pst.calculate_pertubations()



def pestpp_args_test():
    import os
    import pyemu
    pst_dir = os.path.join("pst")
    pst = pyemu.Pst(os.path.join(pst_dir,"br_opt_no_zero_weighted.pst"))
    pst.pestpp_options["lambdas"] = "0.1,0.2,0.3"
    pst.write(os.path.join("temp","temp.pst"))
    pst = pyemu.Pst(os.path.join("temp","temp.pst"))
    print(pst.pestpp_options)


def reweight_test():
    import os
    import numpy as np
    from pyemu import Pst,pst_utils
    pst_dir = os.path.join("pst")
    p = Pst(os.path.join(pst_dir,"pest.pst"))
    obsgrp_dict = {"pred":1.0,"head":1.0,"conc":1.0}
    p.adjust_weights(obsgrp_dict=obsgrp_dict)
    assert np.abs(p.phi - 3.0) < 1.0e-5,p.phi

    obs = p.observation_data
    obs.loc[obs.obgnme=="pred","weight"] = 0.0
    assert np.abs(p.phi - 2.0) < 1.0e-5,p.phi

    obs_dict = {"pd_one":1.0,"pd_ten":1.0}
    p.adjust_weights(obs_dict=obs_dict)
    assert np.abs(p.phi - 4.0) < 1.0e-5,p.phi

def regul_rectify_test():
    import os
    import pyemu
    pst = pyemu.Pst(os.path.join("pst","inctest.pst"))
    pyemu.helpers.zero_order_tikhonov(pst)
    assert pst.prior_information.shape[0] == pst.npar_adj
    pst._update_control_section()
    assert pst.control_data.nprior == pst.prior_information.shape[0]
    fix_names = pst.adj_par_names[::2]
    pst.parameter_data.loc[fix_names,"partrans"] = "fixed"
    pst.rectify_pi()
    assert pst.prior_information.shape[0] == pst.npar_adj
    pst._update_control_section()
    assert pst.control_data.nprior == pst.prior_information.shape[0]


def nnz_groups_test():
    import os
    import pyemu
    pst_dir = os.path.join("pst")
    pst = pyemu.Pst(os.path.join(pst_dir,"br_opt_no_zero_weighted.pst"))
    org_og = pst.obs_groups
    org_nnz_og = pst.nnz_obs_groups
    obs = pst.observation_data
    obs.loc[obs.obgnme==org_og[0],"weight"] = 0.0
    new_og = pst.obs_groups
    new_nnz_og = pst.nnz_obs_groups
    assert org_og[0] not in new_nnz_og


def regdata_test():
    import os
    import pyemu

    pst = pyemu.Pst(os.path.join("pst","pest.pst"))
    phimlim = 10.0
    pst.reg_data.phimlim = phimlim
    pst.control_data.pestmode = "regularization"
    pst.write(os.path.join("temp","pest_regultest.pst"))
    pst_new = pyemu.Pst(os.path.join("temp","pest_regultest.pst"))
    assert pst_new.reg_data.phimlim == phimlim


def from_flopy_test():
    import shutil
    import numpy as np
    try:
        import flopy
    except:
        return
    import pyemu

    new_model_ws = "temp_pst_from_flopy"
    # pilot points for ss in all 3 layers
    # and one set of rch pilot points for the first half of the sim and
    # and one set for the second half of the sim
    pp_props = [["upw.ss",0],["upw.ss",1],["upw.ss",2],\
                ["rch.rech",np.arange(182)],["rch.rech",np.arange(183,365)]]
    #const_props = [["rch.rech",[0,1,2,3,4]],["rch.rech",[-3,-2,-1]]]
    #a single rch const mlt for each stress period
    const_props = [["rch.rech",i] for i in range(365)]
    grid_props = []
    for k in range(3):
        #grid scale pars for hk in all layers
        grid_props.append(["upw.hk",k])
        # const par for hk, ss, sy in all layers
        const_props.append(["upw.hk",k])
        const_props.append(["upw.ss",k])
        const_props.append(["upw.sy",k])

    # zones using ibound values - vka in layer 2
    zone_props = ["upw.vka",1]

    # kper-level multipliers for boundary conditions
    bc_props = [["drn.cond",None]]
    for iper in range(365):
        bc_props.append(["wel.flux",iper])
        bc_props.append(["drn.elev",iper])
    #bc_props = [["wel.flux",None],["drn.cond",None],["drn.elev",None]]

    #org_model_ws = os.path.join("..","..","examples","Freyberg_Truth")
    #nam_file = "freyberg.truth.nam"

    org_model_ws = os.path.join("..","examples","Freyberg_transient")
    nam_file = "freyberg.nam"

    # load the model and reset somethings and write new input
    #m = flopy.modflow.Modflow.load(nam_file,model_ws=org_model_ws)
    #ib = m.bas6.ibound[0].array
    #zn_arr = np.loadtxt(os.path.join("..","..","examples","Freyberg_Truth","hk.zones"),dtype=int)
    #zn_arr[ib<1] = 0
    #m.bas6.ibound = zn_arr

    #m.change_model_ws("temp",reset_external=True)
    #m.name = "freyberg"
    #m.write_input()
    #m.run_model()

    zn_arr = np.loadtxt(os.path.join("..","examples","Freyberg_Truth","hk.zones"),dtype=int)
    k_zone_dict = {k:zn_arr for k in range(3)}
    #smp_sim = os.path.join("utils","TWDB_wells.sim.smp")
    #smp_obs = smp_sim.replace("sim","obs")
    #obssim_smp_pairs = [[smp_obs,smp_sim]]
    obssim_smp_pairs = None
    helper = pyemu.helpers.PstFromFlopyModel(nam_file,org_model_ws,new_model_ws,
                                    pp_props=pp_props,
                                    const_props=const_props,
                                    grid_props=grid_props,
                                    zone_props=zone_props,
                                    bc_props=bc_props,
                                    remove_existing=True,
                                    obssim_smp_pairs=obssim_smp_pairs,
                                    pp_space=4,
                                    use_pp_zones=False,
                                    k_zone_dict=k_zone_dict)
    pst = helper.pst
    obs = pst.observation_data
    obs.loc[:,"weight"] = 0.0
    obs.loc[obs.obsnme.apply(lambda x: x.startswith("cr")),"weight"] = 1.0
    obs.loc[obs.weight>0.0,"obsval"] += np.random.normal(0.0,2.0,pst.nnz_obs)
    pst.control_data.noptmax = 0
    pst.write(os.path.join(new_model_ws,"freyberg_pest.pst"))


def run_array_pars():
    import os
    import pyemu
    new_model_ws = "temp_pst_from_flopy"
    os.chdir(new_model_ws)
    pyemu.helpers.apply_array_pars()
    os.chdir('..')

def add_pi_test():
    import os
    import pyemu
    pst = pyemu.Pst(os.path.join("pst","pest.pst"))
    pst.prior_information = pst.null_prior
    par_names = pst.parameter_data.parnme[:10]
    pst.add_pi_equation(par_names,coef_dict={par_names[1]:-1.0})
    pst.write(os.path.join("temp","test.pst"))

    pst = pyemu.Pst(os.path.join("temp","test.pst"))
    print(pst.prior_information)




if __name__ == "__main__":
    # run_array_pars()
    #from_flopy_test()
    add_pi_test()
    # regdata_test()
    # nnz_groups_test()
    # regul_rectify_test()
    # derivative_increment_tests()
    #tied_test()
    # smp_test()
    # smp_dateparser_test()
    #pst_manip_test()
    # tpl_ins_test()
    #load_test()
    #res_test()
    #smp_test()
    #from_io_with_inschek_test()
    #pestpp_args_test()
    #reweight_test()