import ICluster from cluster_tools
#import pika
#import one
import ConfigHolder
import Runner
import time
import os
import ConfigParser
from stratuslab.Exceptions import OneException

class StratusLabCluster(ICluster):
    
    VM_TARGETSTATE = "Running"
    VM_NODES = "1"

    VM_SHUTDOWN = 60

    ERROR = 1
    
    VM_STATES = {'lcm_init':"Starting",
	 	 'prolog':"Starting",
		 'boot':"Starting",
		 'running':"Running",
		 'migrate':"Running",
		 'save_stop':"Running",
		 'save_suspend':"Running",
		 'save_migrate':"Running",
		 'prolog_migrate':"Starting",
		 'prolog_resume':"Starting",
		 'epilog_stop':"Shutdown",
		 'epilog':"Shutdown",
		 'shutdown':"Shutdown",
		 'cancel':"Shutdown",
		 'failure':"Error",
		 'delete':"Error",
		 'unknown':"Error",
		 
		 'init':"Starting",
		 'pending':"Starting",
		 'hold':"Starting",
		 'active':"Running",
		 'stopped':"Running",
		 'suspended':"Running",
		 'done':"Shutdown",
		 'failed':"Error"
    }
    
#    VM_STATES = {
#         "Prolog"         : "Starting",
#         "Pending"        : "Starting",
#         "Boot"           : "Starting",
#         "Running"        : "Running",
#         "Failed"         : "Error",
#    }
    
    #def __init__(self, name="Dummy Cluster", host="localhost", cloud_type="Dummy",
                 #memory=[], max_vm_mem= -1, cpu_archs=[], networks=[], vm_slots=0,
                 #cpu_cores=0, storage=0,
                 #access_key_id=None, secret_access_key=None, security_group=None,
                 #hypervisor='xen', key_name=None):
	
	## Call super class's init
        #ICluster.__init__(self,name=name, host=host, cloud_type=cloud_type,
                         #memory=memory, max_vm_mem=max_vm_mem, cpu_archs=cpu_archs, networks=networks,
                         #vm_slots=vm_slots, cpu_cores=cpu_cores,
                         #storage=storage, hypervisor=hypervisor)
	#connector = one.OneConnector(pika.PlainCredentials(access_key_id, secret_access_key))
	#connector.setEndpointFromParts('cloud.lal.stratuslab.eu')
    
    #def vm_create(self, vm_name, vm_type="CernVM", vm_user="root", vm_networkassoc="", vm_cpuarch="",
            #vm_image="", vm_mem=1, vm_cores=1, vm_storage=30, customization=None, vm_keepalive=0,
            #job_proxy_file_path=None, myproxy_creds_name=None, myproxy_server=None, 
            #myproxy_server_port=None, job_per_core=False, proxy_non_boot=False,
            #vmimage_proxy_file=None, vmimage_proxy_file_path=None):
	#try:
	    #out = connector.vmStart(vm_name)
	    #new_vm = VM(name = vm_name, id = out, vmtype = vm_type, user = vm_user,
		#network = vm_networkassoc,
		#cpuarch = vm_cpuarch, image = vm_image,
		#memory = vm_mem, cpucores = vm_cores,
		#storage = vm_storage, keep_alive = vm_keepalive, 
		#myproxy_creds_name = myproxy_creds_name, myproxy_server = myproxy_server, 
		#myproxy_server_port = myproxy_server_port, job_per_core = job_per_core)
	    #new_vm = VM(id=out)
	    #self.vms.append(new_vm)
	    #return 0
	#except OneException:
	    #return -1

    #def vm_destroy(self, vm, return_resources=True, reason=""):
	#try:
	    #connector.vmStop(vm.id)            
	    #log.verbose("(vmStop) - workspace shutdown command executed successfully.")
##	    log.verbose("Waiting %ss for VM to shut down..." % self.VM_SHUTDOWN)
##	    time.sleep(self.VM_SHUTDOWN)
##	    log.verbose("Destroying VM")
##	    try:
##		connector.vmKill(vm.id)
##	    except OneException:
##		pass
	    #return 0
	#except OneException:
	    #return -1

    #def vm_poll(self, vm):
	#try:
	    #new_status = connector._vmInfo(vm.id)
		#if vm.status != new_status:
		    #vm.last_state_change = int(time.time())
		    #log.debug("VM: %s on %s. Changed from %s to %s." % (vm.id, self.name, vm.status, new_status))
		    #vm.status = new_status
		#elif vm.override_status != None and new_status:
		    #vm.override_status = None
		    #vm.errorconnect = None

	    #vm.lastpoll = int(time.time())
	    #return vm.status
	#except OneException:
	    #return 'unknown'
	    
    def __init__(self, name="Dummy StratusLab Cluster", host="localhost", cloud_type="StratusLab",
                 memory=[], max_vm_mem= -1, cpu_archs=[], networks=[], vm_slots=0,
                 cpu_cores=0, storage=0,
                 access_key_id=None, secret_access_key=None,
                 hypervisor='xen', key_name=None):
	
	# Call super class's init
        ICluster.__init__(self,name=name, host=host, cloud_type=cloud_type,
                         memory=memory, max_vm_mem=max_vm_mem, cpu_archs=cpu_archs, networks=networks,
                         vm_slots=vm_slots, cpu_cores=cpu_cores,
                         storage=storage, hypervisor=hypervisor)
	
	config = ConfigParser.ConfigParser()
	config.read(os.path.expanduser('~/.stratuslab/stratuslab-user.cfg'))
	
	options = Runner.Runner.defaultRunOptions()
        options.update({'username': config.get('default','username'),
                        'password': config.get('default','password'),
                        'mpi_machine_file': True, 
                        #'instanceType': self.instanceType,
                        'cluster_admin': 'root', 
                        'master_vmid': None,
                        'tolerate_failures': False, 
                        'clean_after_failure': False,
                        'include_master': True, 
                        'shared_folder':'/home',
                        'add_packages': None, 
                        'ssh_hostbased': True, 
                        #'instanceNumber': 0,
                        'verboseLevel':0, 
                        'endpoint':config.get('default','endpoint')})
        configHolder = ConfigHolder.ConfigHolder(options)
        runner = Runner.Runner(key_name, configHolder) #key_name: key in marketplace
	    
    def vm_create(self, vm_name, vm_type="CernVM", vm_user="root", vm_networkassoc="", vm_cpuarch="",
            vm_image="", vm_mem=1, vm_cores=1, vm_storage=30, customization=None, vm_keepalive=0,
            job_proxy_file_path=None, myproxy_creds_name=None, myproxy_server=None, 
            myproxy_server_port=None, job_per_core=False, proxy_non_boot=False,
            vmimage_proxy_file=None, vmimage_proxy_file_path=None):

        log.debug("Running new instance")
        try:
	    ids = runner.runInstance()
	    log.debug("Created instances: " + str(ids))
	    for new_id in ids:
		new_vm = VM(name = vm_name, id = new_id, vmtype = vm_type, user = vm_user,
		    network = vm_networkassoc,
		    cpuarch = vm_cpuarch, image = vm_image,
		    memory = vm_mem, cpucores = vm_cores,
		    storage = vm_storage, keep_alive = vm_keepalive, 
		    myproxy_creds_name = myproxy_creds_name, myproxy_server = myproxy_server, 
		    myproxy_server_port = myproxy_server_port, job_per_core = job_per_core)
		self.vms.append(new_vm)
		try:
		    self.resource_checkout(new_vm)
		except:
		    log.exception("Unexpected error checking out resources when creating a VM. Programming error?")
		    return self.ERROR
	    return 0
	except Exception, e:
	    log.debug("Exception running new instance: " + str(e))
	    return -1

    def vm_destroy(self, vm, return_resources=True, reason=""):
	log.debug("Send shutdown signal to VM " + str(vm.id))
	try:
	    runner.shutdownInstances([vm.id])
	    with self.vms_lock:
		try:
		    self.vms.remove(vm)
		except ValueError:
		    log.error("Attempted to remove vm from list that was already removed.")
		    return_resources = False
	    if return_resources:
		ICluster.resource_return(self, vm)
	    return 0
	except:
	    log.debug("Shutdown error")
	    return -1

    def vm_poll(self, vm):
	try:
	    with self.vms_lock:
		new_status = runner.getVmState(vm.id)
		    if vm.status != new_status:
			vm.last_state_change = int(time.time())
			log.debug("VM: " + str(vm.id) + " on %s. Changed from %s to %s." % (self.name, vm.status, new_status))
			vm.status = new_status
		    elif vm.override_status != None and new_status:
			log.debug("New status for VM " + str(vm.id) + ", override status")
			vm.override_status = None
			vm.errorconnect = None

	    vm.lastpoll = int(time.time())
	    return vm.status
	except OneException, e:
	    log.debug("One exception: " + str(e))
	    return 'shutdown'
	except Exception, e:
	    log.debug("Unknown exception: " + str(e))
	    return 'unknown'