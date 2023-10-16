######################################################################################
#
#   La fonction "sshBackup" permet de sauvegarder 1 dossier,
#		à travers une connexion SSH.
#
######################################################################################
function sshBackup(){ 
	
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

  # Remote path.
	remote_path=''
	
	
	######################################################################################
	#
	#           Gestion de l'aide via l'option -h
	#
	######################################################################################
	
	# Si le script est appelé avec l'option -h, le script devra afficher un message sur la sortie d'erreur indiquant la liste des arguments qu'il attend.
	# getops ?
	usage="usage: sshBackup [-h ssh_host] [-u ssh_user] [-p ssh_port] [-lp local_path] [-rp remote_path] [-v]"
	
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
			# Remote path.
			-rp)
				shift
				remote_path=$1
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
		echo -n "Entrer un chemin de dossier local à synchroniser [.] : " 
		read local_path
		if [[ ! $local_path ]]
		then
			local_path='.'
		fi
	fi
	
  # Remote path :
	if [[ ! $remote_path ]]
	then
		echo -n "Entrer un chemin de dossier distant à synchroniser [.] : " 
		read remote_path
		if [[ ! $remote_path ]]
		then
			remote_path='.'
		fi
	fi
	
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
	
  ######################################################################################
	#
	#           Calcul des valeurs
	#
	######################################################################################
	
	# Current date.
	current_date=`date +%d-%m-%Y`
	
	# Remote folder name.
	remote_folder="$(basename -- $remote_path)"
	
  # Chemin vers le dossier de sauvegarde.
	backup_path="$local_path/$remote_folder-$current_date"
	
	# Chemin vers le fichier compressé.
	tar_path="$backup_path.tar.gz"
	
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
		echo "Remote path = $remote_path"
		echo "Remote folder = $remote_folder"
		echo "Backup tmp path = $backup_path"
		echo "TAR file = $tar_path"
  fi
	
	######################################################################################
	#
	#           Sauvegarde SSH
	#
	######################################################################################
  	
	# Création de la commande de backup SSH.
	ssh_backup="rsync -avz -P -e \"ssh -p $ssh_port\" $ssh_user@$ssh_host:$remote_path $backup_path"
	
	# Création de la commande de compression TAR.
	tar_backup="tar -zcvf $tar_path $backup_path"
	
	# Création de la commande de suppression du dossier temporaire.
	rm_backup="rm -rf $backup_path"
	
  # Verification du dossier local_path
	if [ ! -d $local_path ]
	then
  	# Affichage de la commande SSH.
  	echo "Commande SSH :"
	  echo $ssh_backup
  fi
  
	# Message début.
	echo "Lancement de la sauvegarde SSH :"
	
	# Initiation de la sauvegarde SSH.
	eval $ssh_backup
	
	# Si verbose mode actif.
	if [[ $verbose_mode == 1 ]]
	then 
  	# Info :
	  echo "Récupération terminée."
	  echo "Compression..."
	  # Affichage de la commande TAR.
  	echo "Commande TAR :"
	  echo $tar_backup
	fi
	
  # Initiation de la compression TAR.
	eval $tar_backup
	
	# Si verbose mode actif.
	if [[ $verbose_mode == 1 ]]
	then 
  	# Info :
	  echo "Récupération terminée."
	  echo "Nettoyage..."
	  # Affichage de la commande TAR.
  	echo "Commande de nettoyage :"
	  echo $rm_backup
	fi
	
  # Initiation de la suppression du dossier temporaire.
	eval $rm_backup
	
	# Message fin.
	echo "Sauvegarde terminée. "	
	
	# Retour
	return -1
		
}