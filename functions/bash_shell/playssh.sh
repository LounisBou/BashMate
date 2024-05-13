######################################################################################
#
#   La fonction "playssh" permet de jouer une commande sur le terminale d'une machine distante, 
#   via la création d'un canal SSH.
#
######################################################################################
function playssh(){ 
	
	######################################################################################
	#
	#           Initialisation des variables
	#
	######################################################################################
	
	# Verbose mode.
	verbose_mode=0
	
	# remote host.
	remote_host=''

	# remote SSH user.
	remote_user=''

	# remote SSH port.
	remote_port=''
	
	# command.
	command=''
	
	######################################################################################
	#
	#           Gestion de l'aide via l'option -h
	#
	######################################################################################
	
	# Si le script est appelé avec l'option -h, le script devra afficher un message sur la sortie d'erreur indiquant la liste des arguments qu'il attend.
	# getops ?
	usage="usage: playssh [-h remote_host] [-u remote_user] [-p remote_port] [-c command] [-v] [-ka|--kill-all]"
	
	# Pour chaque options listé 
	while test ${#} -gt 0
	do
				
	  # Switch args.
	  case $1 in
		  # remote host.
			-h)
				shift
				remote_host=$1
			;;
			# remote SSH user.
			-u)
				shift
				remote_user=$1
			;;
			# remote SSH port.
			-p)
				shift
				remote_port=$1
			;;
			# commande.
			-c)
				shift
				command=$1
			;;
			# Kill all ssh command.
			-ka|--kill-all)
				echo "KILL ALL"
				pkill ssh
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
	
	# Remote host:
	if [[ ! $remote_host ]]
	then
		echo -n "Entrer l'IP ou le nom de domaine de la machine distante [localhost] : " 
		read remote_host
		if [[ ! $remote_host ]]
		then
			remote_host='localhost'
		fi
	fi
	
	# Remote SSH user :
	if [[ ! $remote_user ]]
	then
		echo -n "Entrer le nom d'un l'utilisateur SSH de la machine distant [$USER] : " 
		read remote_user
		if [[ ! $remote_user ]]
		then
			remote_user="$USER"
		fi
	fi
	
	# Remote SSH port :
	if [[ ! $remote_port ]]
	then
	#	echo -n "Entrer le port SSH distant [22] : " 
	#	read remote_port
	#	if [[ ! $remote_port ]]
	#	then
			remote_port='22'
	#	fi
	fi
	
	# Command :
	if [[ ! $command ]]
	then
		echo -n "Entrer la commande distante [ls] : " 
		read command
		if [[ ! $command ]]
		then
			command='ls'
		fi
	fi
	
	######################################################################################
	#
	#           Affichage des valeurs
	#
	######################################################################################
	
	# Si verbose mode actif.
	if [[ $verbose_mode == 1 ]]
	then
		# Affichage des valeurs de la commande SCP.
		echo "Remote host = $remote_host"
		echo "Remote SSH user = $remote_user"
		echo "Remote SSH port = $remote_port"
		echo "Commande = $command"
	fi

	
	######################################################################################
	#
	#           Exécution de la commande via SSH.
	#
	######################################################################################
	
	# Commande SSH. 
	ssh="ssh -t $remote_user@$remote_host -p $remote_port "$command" 2>&-"
	
	# Si verbose mode actif.
	if [[ $verbose_mode == 1 ]]
	then 
		# Affichage de la commande SCP.
		echo "Lancement de la commande via SSH :"
		echo $ssh
	fi
	
	# Initiation de la commande via SSH en mode background.
	eval $ssh
	
	# Retour
	return -1
	
}