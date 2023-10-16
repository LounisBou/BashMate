######################################################################################
#
#   La fonction "backd" permet de transférer le port d'une machine locale,
#		vers le port d'une machine distante à travers une connexion SSH.
# 	Elle peut être appeler autant de fois que l'on souhaite (1 fois par port de la machine distante)
# 	Pour stopper le tunneling faire : backd --kill-all
#
######################################################################################
function backd(){ 
	
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

	# Local host.
	local_host=''

	# Local port.
	local_port=''

	# Remote port.
	remote_port=''
	
	######################################################################################
	#
	#           Gestion de l'aide via l'option -h
	#
	######################################################################################
	
	# Retrieve process list.
	process_list=($(ps aux | grep -i 'ssh -fN -R' | grep -v grep | tr -s ' '  | cut -d ' ' -f 2))
	process_list=($process_list)
	
  # Get process count.
	nb_process="${#process_list[@]}"
	#echo $nb_process
  
	# Retrieve process info.
  user_list=($(ps aux | grep -i 'ssh -fN -R' | grep -v grep | tr -s ' '  | cut -d ' ' -f 1))
  pid_list=($(ps aux | grep -i 'ssh -fN -R' | grep -v grep | tr -s ' '  | cut -d ' ' -f 2))
  ssh_host_list=($(ps aux | grep -i 'ssh -fN -R' | grep -v grep | tr -s ' '  | cut -d ' ' -f 15))
  ssh_port_list=($(ps aux | grep -i 'ssh -fN -R' | grep -v grep | tr -s ' '  | cut -d ' ' -f 17))
  tunnel_list=($(ps aux | grep -i 'ssh -fN -R' | grep -v grep | tr -s ' '  | cut -d ' ' -f 14))			
	
	
	######################################################################################
	#
	#           Gestion de l'aide via l'option -h
	#
	######################################################################################
	
	# Si le script est appelé avec l'option -h, le script devra afficher un message sur la sortie d'erreur indiquant la liste des arguments qu'il attend.
	# getops ?
	usage="usage: backd [-h ssh_host] [-u ssh_user] [-p ssh_port] [-lh local_host] [-lp local_port] [-rp remote_port] [-v] [-l|--list] [-k] [-ka|--kill-all]"
	
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
			# Local host.
			-lh)
				shift
				local_host=$1
			;;
			# Local port.
			-lp)
				shift
				local_port=$1
			;;
			# Remote port.
			-rp)
				shift
				remote_port=$1
			;;
			# list all ssh tunnel.
			-l|--list|-k)
			
				# If no process.
        	if [[ $nb_process == 0 ]]
        	then
        	  echo "Aucun tunnel en cours."	
        	  return -1
        fi
			
				# Retrieve process list.
				echo "SSH Tunnel list : "
				
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
          tunnel=${tunnel_list[$i]}
          # Echo process.
          echo "Tunnel #$i : $ssh_host:$ssh_port => $tunnel [$user]"
        done
        
        # Kill mode.
        if [[ $1 == '-k' ]]
        then
          echo "Entrer le numéro de proxy à stopper : "
          read number
          if [[ $number > $nb_process ]]
          then
            echo "Le tunnel demandé n'existe pas. Fin de commande."
            return -1
          fi
          # Get proxy process pid.
          pid=${pid_list[$number]}
          # Kill ask process.
          kill $pid
        fi
        
        # End.
				return -1
				
			;;
			# Kill all ssh command.
			-ka|--kill-all)
				echo "KILL ALL"
				pkill ssh -fN -R
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
	
	# Local host :
	if [[ ! $local_host ]]
	then
		local_host='localhost'
	fi
	
	# Local port :
	if [[ ! $local_port ]]
	then
		local_port='22'
	fi
	
	# Remote port :
	if [[ ! $remote_port ]]
	then
		remote_port='2222'
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
		echo "Local host = $local_host"
		echo "Local port = $local_port"
		echo "Remote port = $remote_port"
	fi
	
  ######################################################################################
	#
	#           Controles
	#
	######################################################################################
	
	# Si tunnel déjà ouvert.
	tunnel_value="$remote_port:$local_host:$local_port"
	if [[ " ${tunnel_list[*]} " == *"$tunnel_value"* ]]
	then
    echo "Un tunnel est déjà ouvert : [$tunnel_value]"
    return -1
  fi
	
	######################################################################################
	#
	#           Tunnel SSH
	#
	######################################################################################
	
	# Création de la commande de tunnel SSH. (-fN = -f + -N)
	# -f : Go in background mode after connexion.
	# -N : No command to lauch in background mode.
	sshbackd="ssh -fN -R $remote_port:$local_host:$local_port $ssh_user@$ssh_host -p $ssh_port"
	
	# Si verbose mode actif.
	if [[ $verbose_mode == 1 ]]
	then 
		# Affichage de la commande SSH.
		echo "Lancement de la commande SSH :"
		echo $sshbackd
	fi
	
	# Initiation du tunnel SSH en mode background.
	eval $sshbackd
	echo "Back door ouverte : $ssh_host:$remote_port"
	
	# Retour
	return -1
	
}