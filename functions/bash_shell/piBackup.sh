######################################################################################
#
#   La fonction "piBackup" permet de sauvegarder une carte SD de raspberry pi,
#		à travers une connexion SSH.
#
######################################################################################
function piBackup(){ 
	
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
	
  # Local path.
	local_path=''

	
	######################################################################################
	#
	#           Gestion de l'aide via l'option -h
	#
	######################################################################################
	
	# Si le script est appelé avec loption -h, le script devra afficher un message sur la sortie derreur indiquant la liste des arguments quil attend.
	# getops ?
	usage="usage: piBackup [-h ssh_host] [-u ssh_user] [-p ssh_port] [-lp local_path] [-v]"
	
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
			# Local path.
			-lp)
				shift
				local_path=$1
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
		echo -n "Entrer le port d'écoute du serveur SSH de la machine distante [22] : " 
		read ssh_port
		if [[ ! $ssh_port ]]
		then
			ssh_port='22'
		fi
	fi
	
	# Local path :
	if [[ ! $local_path ]]
	then
		echo -n "Entrer un chemin de dossier local pour la sauvegarde [.] : " 
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
		# Affichage des valeurs de la commande SSH.
		echo "SSH host = $ssh_host"
		echo "SSH user = $ssh_user"
		echo "SSH port = $ssh_port"
		echo "Local path = $local_path"
	fi

	
	######################################################################################
	#
	#           Sauvegarde SSH
	#
	######################################################################################
	
	# Verification du dossier local_path
	if [ ! -d $local_path ]
	then
		# Si verbose mode actif.
  	if [[ $verbose_mode == 1 ]]
  	then 
      echo "Création du dossier de sauvegarde : $local_path"
    fi
    mkdir $local_path
  fi
	
	# Current date.
	current_date=`date +%d-%m-%Y`
	
	# Chemin vers le fichier de sauvegarde.
	backup_path="$local_path/$ssh_host-$current_date.gz"
	
	# Création de la commande de backup SSH.
	ssh_backup="ssh $ssh_user@$ssh_host -p $ssh_port \"sudo dd if=/dev/mmcblk0 bs=1M | gzip -\" | dd of=$backup_path"
	
  # Verification du dossier local_path
	if [ ! -d $local_path ]
	then
  	# Affichage de la commande SSH.
  	echo "Command SSH :"
	  echo $ssh_backup
  fi
  
	# Message début.
	echo "Lancement de la sauvegarde SSH :"
	
	# Initiation de la sauvegarde SSH.
	eval $ssh_backup
	
	# Message fin.
	echo "Sauvegarde terminée. "	
	
	# Retour
	return -1
	
}