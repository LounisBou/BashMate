######################################################################################
#
#   La fonction "get" permet de récupérer un dossier ou fichier depuis une machine distante,
#		l'accès à la machine distante se fait via le protocole SSH, et le transfert via à la commande SCP.
#
######################################################################################
function get(){ 
	
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
	
	# remote path.
	remote_path=''
	
	# Local path.
	local_path=''
	
	######################################################################################
	#
	#           Gestion de l'aide via l'option -h
	#
	######################################################################################
	
	# Si le script est appelé avec l'option -h, le script devra afficher un message sur la sortie d'erreur indiquant la liste des arguments qu'il attend.
	# getops ?
	usage="usage: get [-h remote_host] [-u remote_user] [-p remote_port] [-rp remote_path] [-lp local_path] [-v] [-ka|--kill-all]"
	
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
			# remote path.
			-rp)
				shift
				remote_path=$1
			;;
			# Local path.
			-lp)
				shift
				local_path=$1
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
	
	# Remote path :
	if [[ ! $remote_path ]]
	then
		echo -n "Entrer le chemin distant [.] : " 
		read remote_path
		if [[ ! $remote_path ]]
		then
			remote_path='.'
		fi
	fi
	
	# Local path :
	if [[ ! $local_path ]]
	then
		echo -n "Entrer le chemin local [.] : " 
		read local_path
		if [[ ! $local_path ]]
		then
			local_path='.'
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
		echo "Remote path = $remote_path"
		echo "Local path = $local_path"
	fi

	
	######################################################################################
	#
	#           Copie via la commande SCP
	#
	######################################################################################
	
	# Commande SCP. 
	scp="scp -P $remote_port -r -p $remote_user@$remote_host:$remote_path $local_path"
	

	# Si verbose mode actif.
	if [[ $verbose_mode == 1 ]]
	then 
		# Affichage de la commande SCP.
		echo "Lancement de la commande SCP :"
		echo $scp
	fi
	
	# Initiation de la commande SCP en mode background.
	eval $scp
	
	# Retour
	return -1
	
}