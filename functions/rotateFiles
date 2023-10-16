######################################################################################
#
#   La fonction "rotateFiles" de nettoyer un dossier des fichiers et sous-dossiers,
#		à partir d'une date de création, modification, accès.
#
######################################################################################
function rotateFiles(){ 
	
	######################################################################################
	#
	#           Initialisation des variables
	#
	######################################################################################
	
	# Verbose mode.
	verbose_mode=0
	
	# Rotate time.
	rotate_time=''
	
  # Time mode.
	time_mode=''

	# Rotate mode.
	rotate_mode=''
	
  # Rotate path.
	rotate_path=''
	
  # Backup path.
	backup_path=''
	
	######################################################################################
	#
	#           Gestion de l'aide via l'option -h
	#
	######################################################################################
	
	# Si le script est appelé avec l'option -h, le script devra afficher un message sur la sortie d'erreur indiquant la liste des arguments qu'il attend.
	# getops ?
	usage="usage: rotateFiles [-t rotate_time] [-tm time_mode] [-rm rotate_mode] [-p rotate_path] [-bp backup_path] [-v]"
	
	# Pour chaque options listé 
	while test ${#} -gt 0
	do
				
	  # Switch args.
	  case $1 in
		  # Time.
			-t)
				shift
				rotate_time=$1
			;;
			# Time mode.
			-tm)
				shift
				time_mode=$1
			;;
			# Rotate mode.
			-rm)
				shift
				rotate_mode=$1
			;;
			# Rotate files path.
			-p)
				shift
				rotate_path=$1
			;;
			# Backup path.
			-bp)
				shift
				backup_path=$1
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
	
	# Time :
	if [[ ! $rotate_time ]]
	then
		echo -n "Entrer le nombre de jour d'ancienneté à néttoyer [365] : " 
		read rotate_time
		if [[ ! $rotate_time ]]
		then
			rotate_time=365
		fi
	fi
	
  # Time mode :
	if [[ ! $time_mode ]]
	then
		echo -n "Entrer le mode de calcul de l'ancienneté. [c (created)/m (modified)/a (accessed)] : " 
		read time_mode
		if [[ $time_mode != 'c' && $time_mode != 'm' && $time_mode != 'a' ]]
		then
		  echo "Error : Mode de calcul de l'ancienneté non valide."
		  echo "Nettoyage avorté."
			return -1
		fi
	fi
	
  # Rotate mode :
	if [[ ! $rotate_mode ]]
	then
		echo -n "Entrer le mode de rotation des fichiers. [d (delete)/m (move)/c (copy)] : " 
		read rotate_mode
		if [[ $rotate_mode != 'd' && $rotate_mode != 'm' && $rotate_mode != 'c' ]]
		then
		  echo "Error : Mode de calcul de l'ancienneté non valide."
		  echo "Nettoyage avorté."
			return -1
		fi
	fi
	
	# Rotate path :
	if [[ ! $rotate_path ]]
	then
		echo -n "Entrer le dossier à nettoyer [.] : " 
		read rotate_path
		if [[ ! $rotate_path ]]
		then
			rotate_path='.'
		fi
	fi
	
  # Backup path :
	if [[ ! $backup_path ]]
	then
		echo -n "Entrer le dossier de sauvegarde [.] : " 
		read backup_path
		if [[ ! $backup_path ]]
		then
			backup_path='.'
		fi
	fi
	
  ######################################################################################
	#
	#           Dossier de backup
	#
	######################################################################################
	
	# If rotate mode move or copy.
	if [[ $rotate_mode != 'd' ]] 
	then
  	# Si dossier backup non existant.
  	if [ ! -d $backup_path ]
  	then
    	# Commande de création du dossier.
    	mkdir_cmd="mkdir $backup_path"
  		# Si verbose mode actif.
    	if [[ $verbose_mode == 1 ]]
    	then 
      	  echo "[Warning] Le dossier local n'existe pas."
        echo "[Info] Création du dossier local."
        echo "$mkdir_cmd"
      fi
      # Création du dossier.
      eval $mkdir_cmd
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
		echo "Rotate time = $rotate_time"
		echo "Time mode = $time_mode"
		echo "Rotate mode = $rotate_mode"
		echo "Rotate path = $rotate_path"
		echo "Backup path = $backup_path"
	fi
  
	
	######################################################################################
	#
	#           Nettoyage par rotation
	#
	######################################################################################
	
	# Time mode real value.
	if [[ $time_mode == 'c' ]] 
	then
  	time_mode="ctime"
  elif [[ $time_mode == 'm' ]]
  then
    time_mode="mtime"
  elif [[ $time_mode == 'a' ]]
  then  
    time_mode="atime"
	fi
	
  # Rotate command.
	if [[ $rotate_mode == 'd' ]] 
	then
  	rotate_cmd="rm -rf \"{}\""
  elif [[ $rotate_mode == 'm' ]]
  then
    rotate_cmd="mv \"{}\" $backup_path/"
  elif [[ $rotate_mode == 'c' ]]
  then  
    rotate_cmd="cp -R \"{}\" $backup_path/"
	fi
	
  # Commande de nettoyage.
  rotate_cmd="/usr/bin/find $rotate_path/* -name \"*\" -$time_mode +$rotate_time -exec rm -rf $backup_path \;"
  
  # Si verbose mode actif.
	if [[ $verbose_mode == 1 ]]
	then	  
	  echo "Command : $rotate_cmd"
  fi
  
	# Message début.
	echo "Lancement de la rotation :"
	
	# Initiation de la rotation.
	eval $rotate_cmd
	
	# Message fin.
	echo "Rotation terminé."	
	
	# Retour
	return -1
	
}