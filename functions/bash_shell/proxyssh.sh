######################################################################################
#
#   La fonction "proxyssh" permet de créer un tunnel ssh ainsi qu'un proxy socks5
#		à travers une connexion SSH.
# 	Elle peut être appeler autant de fois que l'on souhaite (1 fois par port)
# 	Pour stopper le proxy faire : proxyssh --kill-all
#
######################################################################################
function proxyssh(){ 
	
	######################################################################################
	#
	#           Initialisation des variables
	#
	######################################################################################
	
	# Verbose mode.
	verbose_mode=0
	
	# SSH Host.
	ssh_host=''

	# SSH User.
	ssh_user=''

	# SSH Port.
	ssh_port=''

	# Proxy port.
	proxy_port=''
	
	# MAC OS proxy.
	mac_proxy=''
	
	# MAC OS active interface.
	mac_interface='Wi-Fi'
	
  ######################################################################################
	#
	#           Retrieve process states.
	#
	######################################################################################
	
	# Retrieve process list.
	process_list=($(ps aux | grep -i 'ssh -fN -D' | grep -v grep | tr -s ' '  | cut -d ' ' -f 2))
	process_list=($process_list)
	
	# Get process count.
	nb_process="${#process_list[@]}"
	#echo $nb_process
	
	# Retrueve process info.
  user_list=($(ps aux | grep -i 'ssh -fN -D' | grep -v grep | tr -s ' '  | cut -d ' ' -f 1))
  pid_list=($(ps aux | grep -i 'ssh -fN -D' | grep -v grep | tr -s ' '  | cut -d ' ' -f 2))
  ssh_host_list=($(ps aux | grep -i 'ssh -fN -D' | grep -v grep | tr -s ' '  | cut -d ' ' -f 15))
  ssh_port_list=($(ps aux | grep -i 'ssh -fN -D' | grep -v grep | tr -s ' '  | cut -d ' ' -f 17))
  proxy_port_list=($(ps aux | grep -i 'ssh -fN -D' | grep -v grep | tr -s ' '  | cut -d ' ' -f 14))
	
	######################################################################################
	#
	#           Gestion de l'aide via l'option -h
	#
	######################################################################################
	
	# Si le script est appelé avec loption -h, le script devra afficher un message sur la sortie derreur indiquant la liste des arguments quil attend.
	# getops ?
	usage="usage: proxyssh [-h ssh_host] [-u ssh_user] [-p ssh_port] [-pp proxy_port] [-mp|--mac-proxy] [-v] [-l|--list] [-k] [-ka|--kill-all]"
	
	# Pour chaque options listé 
	while test ${#} -gt 0
	do
				
	  # Switch args.
	  case $1 in
		  # SSH Host.
			-h)
				shift
				ssh_host=$1
			;;
			# SSH User.
			-u)
				shift
				ssh_user=$1
			;;
			# SSH Port.
			-p)
				shift
				ssh_port=$1
			;;
			# Proxy port.
			-pp)
				shift
				proxy_port=$1
			;;
			# Mac os proxy.
			-mp|--mac-proxy)
			  shift
				mac_proxy=$1
      ;;
			# list all ssh proxy.
			-l|--list|-k)
			
			
				# If no process.
        	if [[ $nb_process == 0 ]]
        	then
        	  echo "Aucun proxy SSH en cours."	
        	  return -1
        fi
        
			  # Retrieve process list.
				echo "SSH Proxy : "
				
				# Loop over process list.				
				for ((i=1;i<=$nb_process;i++))
        do
          # Retrieve process line from process array.
          process=${process_list[$i]}
          # Retrieve process info from line.
          user=${user_list[$i]}
          pid=${pid_list[$i]}
          ssh_host=${ssh_host_list[$i]}
          ssh_port=${ssh_port_list[$i]}
          proxy_port=${proxy_port_list[$i]}
          # Echo process.
          echo "Proxy #$i : $ssh_host:$ssh_port => localhost:$proxy_port [$user]"
        done
        
        # Kill mode.
        if [[ $1 == '-k' ]]
        then
          echo "Entrer le numéro de proxy à stopper : "
          read number
          if [[ $number > $nb_process ]]
          then
            echo "Le proxy demandé n'existe pas. Fin de commande."
            return -1
          fi
          # Get proxy process pid.
          pid=${pid_list[$number]}
          # Kill ask process.
          kill $pid && echo "Proxy #$number have been stop."
          # Mac proxy désactivation.
          networksetup -setsocksfirewallproxystate $mac_interface off && echo "Configuration proxy du mac désactivée."
        fi
        
        # End.
				return -1
				
			;;
			# Kill all ssh command.
			-ka|--kill-all)
			  # Kill all proxy process.
				pkill ssh -fN -D && echo "All proxy have been stop."
				# Mac proxy désactivation.
        networksetup -setsocksfirewallproxystate $mac_interface off && echo "Configuration proxy du mac désactivée."
				return -1
			;;
			# Verbose.
			-v)
				verbose_mode=1
				echo "Mode verbose activé."
			;;
			#Usage.
			*)   
				if [[ $1 ]]
				then 
					echo "$1 n'est pas une option valide."
					echo "$usage"
					return -1 
				fi
			;;
		esac
		
		# Décallage des arguments.
		shift
		
	done


	######################################################################################
	#
	#           Gestion des valeurs par défaut
	#
	######################################################################################
	
	# Host SSH :
	if [[ ! $ssh_host ]]
	then
		echo -n "Entrer l'IP ou le nom de domaine du serveur auquel vous souhaitez vous connecter [localhost] : " 
		read ssh_host
		if [[ ! $ssh_host ]]
		then
			ssh_host='localhost'
		fi
	fi
	
	# User SSH :
	if [[ ! $ssh_user ]]
	then
		echo -n "Entrer le nom d'un l'utilisateur autorisé à se connecter en SSH à la machine distante [$USER] : " 
		read ssh_user
		if [[ ! $ssh_user ]]
		then
			ssh_user="$USER"
		fi
	fi
	
	# Port SSH :
	if [[ ! $ssh_port ]]
	then
		ssh_port='22'
	fi
	
	# Proxy port :
	if [[ ! $proxy_port ]]
	then
		proxy_port='8085'
	fi
	
	######################################################################################
	#
	#           Affichage des valeurs
	#
	######################################################################################
	
	# Si verbose mode actif.
	if [[ $verbose_mode == 1 ]]
	then
		# Affichage des valeurs de la commande SSH.
		echo "SSH host = $ssh_host"
		echo "SSH user = $ssh_user"
		echo "SSH port = $ssh_port"
		echo "Proxy port = $proxy_port"
	fi
	
  ######################################################################################
	#
	#           Controles
	#
	######################################################################################
	
	# Si port déjà utilisé.
	if [[ " ${proxy_port_list[@]} " =~ " ${proxy_port} " ]]
	then
    echo "Un proxy tourne déjà sur le port demandé : [$proxy_port]"
    return -1
  fi
  
  # Activation du proxy de MAC OS.
  if [[ $mac_proxy == 'on' ]]
  then
    
    if not (networksetup -setsocksfirewallproxy $mac_interface localhost $proxy_port) ;
    then
      # Mac network OS interface no found.
      echo "L'interface configurer dans la commande proxy est érronée. Choisissez une interface dans la liste ci-dessous et la commande proxyssh."
      # List interface.
      echo "Liste des interfaces disponible : "
      networksetup -listnetworkserviceorder
      return -1
    fi
    
  	# Définition du port d'écoute du proxy de MAC OS.
  	networksetup -setsocksfirewallproxy $mac_interface localhost $proxy_port
  	# Mac proxy activation.
    networksetup -setsocksfirewallproxystate $mac_interface on && echo "Configuration proxy du MAC activée."
  fi
  
  # Désctivation du proxy de MAC OS.
  if [[ $mac_proxy == 'off' ]]
  then
    # Mac proxy désactivation.
    networksetup -setsocksfirewallproxystate $mac_interface off && echo "Configuration proxy du MAC désactivée."
  fi
	
	######################################################################################
	#
	#           Proxy SSH
	#
	######################################################################################
	
	# Création de la commande de proxy SSH. (-fN = -f + -N)
	# -f : Go in background mode after connexion.
	# -N : No command to lauch in background mode.
	sshproxy="ssh -fN -D $proxy_port $ssh_user@$ssh_host -p $ssh_port"
	
	# Si verbose mode actif.
	if [[ $verbose_mode == 1 ]]
	then 
		# Affichage de la commande SSH.
		echo "Lancement de la commande SSH :"
		echo $sshproxy
	fi
	
	# Initiation du proxy SSH en mode background.
	eval $sshproxy 
	echo "Proxy démarré. En écoute sur le port $proxy_port..."
	
	# Retour
	return -1
	
}