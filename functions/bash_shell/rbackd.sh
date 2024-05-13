######################################################################################
#
#   La fonction "rbackd" permet de transférer le port d'une machine distante,
#		vers le port d'une seconde machine distante à travers une connexion SSH.
# 	Elle peut être appeler autant de fois que l'on souhaite (1 fois par port de la machine distante)
# 	Pour stopper les backd faire : rbackd --kill-all
#
######################################################################################
function rbackd(){ 
	
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
	
	# Backd SSH Host.
	bd_ssh_host=''

	# Backd SSH User.
	bd_ssh_user=''

	# Backd SSH Port.
	bd_ssh_port=''

	# Backd Local host.
	bd_local_host=''

	# Backd Local port.
	bd_local_port=''

	# Backd Remote port.
	bd_remote_port=''
	
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
  backd_list=($(ps aux | grep -i 'ssh -fN -R' | grep -v grep | tr -s ' '  | cut -d ' ' -f 14))			
	
	
	######################################################################################
	#
	#           Gestion de l'aide via l'option -h
	#
	######################################################################################
	
	# Si le script est appelé avec l'option -h, le script devra afficher un message sur la sortie d'erreur indiquant la liste des arguments qu'il attend.
	# getops ?
	usage="usage: rbackd [-h ssh_host] [-u ssh_user] [-p ssh_port] [-bh backd_ssh_host] [-bu backd_ssh_user] [-bp backd_ssh_port] [-blh backd_local_host] [-blp backd_local_port] [-brp backd_remote_port] [-v] [-l|--list] [-k] [-ka|--kill-all]"
	
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
		  # Backd SSH Host.
			-bh)
				shift
				bd_ssh_host=$1
			;;
			# Backd SSH User.
			-bu)
				shift
				bd_ssh_user=$1
			;;
			# Backd SSH Port.
			-bp)
				shift
				bd_ssh_port=$1
			;;
			# Backd Local host.
			-blh)
				shift
				bd_local_host=$1
			;;
			# Backd Local port.
			-blp)
				shift
				bd_local_port=$1
			;;
			# Backd Remote port.
			-brp)
				shift
				bd_remote_port=$1
			;;
			# list all ssh backd.
			-l|--list|-k)
			
				# If no process.
        	if [[ $nb_process == 0 ]]
        	then
        	  echo "Aucun backd en cours."	
        	  return -1
        fi
			
				# Retrieve process list.
				echo "SSH backd list : "
				
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
          backd=${backd_list[$i]}
          # Echo process.
          echo "Backd #$i : $ssh_host:$ssh_port => $backd [$user]"
        done
        
        # Kill mode.
        if [[ $1 == '-k' ]]
        then
          echo "Entrer le numéro de backd à stopper : "
          read number
          if [[ $number > $nb_process ]]
          then
            echo "Le backd demandé n'existe pas. Fin de commande."
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
	
	# Backd Host SSH :
	if [[ ! $bd_ssh_host ]]
	then
		echo -n "Entrer l'IP ou le nom de domaine du serveur backd [localhost] : " 
		read bd_ssh_host
		if [[ ! $bd_ssh_host ]]
		then
			bd_ssh_host='localhost'
		fi
	fi
	
	# Backd User SSH :
	if [[ ! $bd_ssh_user ]]
	then
		echo -n "Entrer le nom d'un l'utilisateur sur le serveur backd [$USER] : " 
		read bd_ssh_user
		if [[ ! $bd_ssh_user ]]
		then
			bd_ssh_user="$USER"
		fi
	fi
	
	# Backd Port SSH :
	if [[ ! $bd_ssh_port ]]
	then
		bd_ssh_port='22'
	fi
	
	# Backd Local host :
	if [[ ! $bd_local_host ]]
	then
		bd_local_host='localhost'
	fi
	
	# Backd Local port :
	if [[ ! $bd_local_port ]]
	then
		bd_local_port=$ssh_port
	fi
	
	# Backd Remote port :
	if [[ ! $bd_remote_port ]]
	then
		bd_remote_port='2020'
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
		echo "Backd SSH host = $bd_ssh_host"
		echo "Backd SSH user = $bd_ssh_user"
		echo "Backd SSH port = $bd_ssh_port"
		echo "Backd Local host = $bd_local_host"
		echo "Backd Local port = $bd_local_port"
		echo "Backd Remote port = $bd_remote_port"
	fi
	
  ######################################################################################
	#
	#           Controles
	#
	######################################################################################
	
	# Si backd déjà ouvert.
	backd_value="$remote_port:$local_host:$local_port"
	if [[ " ${backd_list[*]} " == *"$backd_value"* ]]
	then
    echo "Une backd est déjà ouvert : [$backd_value]"
    return -1
  fi
	
	######################################################################################
	#
	#           Backd SSH
	#
	######################################################################################
	
	# Création de la commande SSH. 
	sshrbackd="ssh -fN $ssh_user@$ssh_host -p $ssh_port ssh -fN -R $bd_remote_port:$bd_local_host:$bd_local_port $bd_ssh_user@$bd_ssh_host -p $bd_ssh_port -i .ssh/id_rsa_backd" 
	
	# Si verbose mode actif.
	if [[ $verbose_mode == 1 ]]
	then 
		# Affichage de la commande SSH.
		echo "Lancement de la commande SSH :"
		echo $sshrbackd
	fi
	
	# Copie des clefs SSH local. 
	scp -P $ssh_port -r -p ~/.ssh/id_rsa $ssh_user@$ssh_host:~/.ssh/id_rsa_backd && echo "Clefs SSH copiées."
	
	# Autorisation id_rsa.
	ssh -t $ssh_user@$ssh_host -p $ssh_port "chmod 400 .ssh/id_rsa_backd" 2>&- && echo "Clefs SSH accéssible." 
	
	# Initiation de la backd SSH en mode background.
	eval $sshrbackd
	echo "Remote backd ouverte : $bd_ssh_user@$bd_ssh_host"
	
  # Suppression des clefs SSH.
  ssh -t $ssh_user@$ssh_host -p $ssh_port "chmod 777 .ssh/id_rsa_backd" 2>&- && echo "Clefs SSH accéssible." 
	ssh -t $ssh_user@$ssh_host -p $ssh_port rm -rf ~/.ssh/id_rsa_backd && echo "Clefs SSH supprimées."
	
	# Retour
	return -1
	
}