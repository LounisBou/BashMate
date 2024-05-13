######################################################################################
#
#   La fonction "findin" permet de rechercher une chaine de caractère à travers fichiers d'un répertoire de façon récursive.
#
######################################################################################
function findin(){ 
	
	######################################################################################
	#
	#           Initialisation des variables
	#
	######################################################################################
	
	# Verbose mode.
	verbose_mode=0
	
	# search string.
	search_str=''

  # search path.
	search_path=''
	
	# search extension.
	search_ext=''
	
	######################################################################################
	#
	#           Gestion de l'aide via l'option -h
	#
	######################################################################################
	
	# Si le script est appelé avec l'option -h, le script devra afficher un message sur la sortie d'erreur indiquant la liste des arguments qu'il attend.
	# getops ?
	usage="usage: get [-e|--ext file_extension] [-v verbose] [-h|--help usage] [search_path] search_string"
	
	# Pour chaque options listé 
	while test ${#} -gt 0
	do
				
	  # Switch args.
	  case $1 in
			# Search file extension.
			-e|--ext)
				shift
				search_ext=$1
			;;
			# Verbose.
			-v)
				verbose_mode=1
				echo "Mode verbose activé."
			;;
			# Usage.
			-h|--help)   
				if [[ $1 ]]
				then 
					echo "$usage"
					return -1 
				fi
			;;
      # Search string and path.
			*)
				if [[ ! $search_str ]]
				then
				  search_str=$1
				elif [[ ! $search_path ]]
				then
				  # Switch les variables.
				  search_path=$search_str
				  search_str=$1
				else
				  echo "Nombre de paramètre invalide."
				  # Si verbose mode actif.
          if [[ $verbose_mode == 1 ]]
          then
  				  echo "Search path : $search_path"
  				  echo "Search string : $search_str"
  				  echo "Search file extension : $search_ext"
  				fi
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
		
  # Vérification recherche non null :
	if [[ ! $search_str ]]
	then
		echo "Vous devez saisir une chaine de caractère à rechercher."
		echo "$usage"
		return -1 
	fi
	
  # Vérification du chemin par défaut :
	if [[ ! $search_path ]]
	then
		search_path="." 
	fi
	
	# Prefixe de l'extension :
	if [[ $search_ext ]]
	then
    search_ext=".$search_ext"
	fi

	
	######################################################################################
	#
	#           Affichage des valeurs
	#
	######################################################################################
	
	# Si verbose mode actif.
	if [[ $verbose_mode == 1 ]]
	then
		# Affichage des valeurs de la commande find.
		echo "Search path = $search_path"
		echo "Search string = $search_str"
		echo "Search file extension = $search_ext"
	fi

	
	######################################################################################
	#
	#           Recherche via la commande find
	#
	######################################################################################
	
	# Commande find. 
  find="sudo find $search_path -name \"*$search_ext\" -exec sudo grep -d skip -li $search_str '{}' ';'"

	# Si verbose mode actif.
	if [[ $verbose_mode == 1 ]]
	then 
		# Affichage de la commande find.
		echo "Lancement de la commande find :"
		echo $find
	fi
	
	# Initiation de la commande find.
	eval $find

	
	# Retour
	return -1
	
}
