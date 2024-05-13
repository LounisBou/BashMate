# Man page for tunssh.
# .\" Manpage for tunssh.
# .TH man 1 "1.0" "tunssh man page"
# .SH NAME
# tunssh \- transfer remote port to local port through SSH
# .SH SYNOPSIS
# tunssh [-h ssh_host] [-u ssh_user] [-p ssh_port] [-rth remote_tunnel_host] [-rtp remote_tunnel_port] [-ltp local_tunnel_port] [-v] [-l|--list] [-k] [-ka|--kill-all]
# .SH DESCRIPTION
# The tunssh transfer remote port to local port through SSH.
# tunssh can be called as many times as you want (1 time per port).
# To stop tunneling do: tunssh --kill-all
# .SH OPTIONS
# tunssh accepts the following options:
# -h
#     SSH Host.
# -u
#     SSH User.
# -p
#     SSH Port.
# -rth
#     Remote tunnel host.
# -rtp
#     Remote tunnel port.
# -ltp
#     Local tunnel port.
# -v
#     Verbose mode.
# -l|--list
#     List all ssh tunnel.
# -k
#     Kill a ssh tunnel.
# -ka|--kill-all
#     Kill all ssh tunnel.
# .SH BUGS
# No known bugs.
# .SH AUTHOR
# LounisBou (lounis.bou@gmail.com)
# "
#
# ! TUNSSH
#
function tunssh(){ 
    
    # ! Initialize variables.
    
    # Verbose mode.
    verbose_mode=0
    
    # SSH Host.
    ssh_host=''

    # SSH User.
    ssh_user=''

    # SSH Port.
    ssh_port=''

    # Remote tunnel host.
    remote_tunnel_host=''

    # Local tunnel port.
    local_tunnel_port=''

    # Remote tunnel port.
    remote_tunnel_port=''
    
    # ! Retrieve process list.
    
    # Retrieve process list.
    process_list=($(ps aux | grep -i 'ssh -fN -L' | grep -v grep | tr -s ' '  | cut -d ' ' -f 2))
    process_list=($process_list)
    
    # Get process count.
    nb_process="${#process_list[@]}"
    #echo $nb_process
  
    # Retrieve process info.
    user_list=($(ps aux | grep -i 'ssh -fN -L' | grep -v grep | tr -s ' '  | cut -d ' ' -f 1))
    pid_list=($(ps aux | grep -i 'ssh -fN -L' | grep -v grep | tr -s ' '  | cut -d ' ' -f 2))
    ssh_host_list=($(ps aux | grep -i 'ssh -fN -L' | grep -v grep | tr -s ' '  | cut -d ' ' -f 15))
    ssh_port_list=($(ps aux | grep -i 'ssh -fN -L' | grep -v grep | tr -s ' '  | cut -d ' ' -f 17))
    tunnel_list=($(ps aux | grep -i 'ssh -fN -L' | grep -v grep | tr -s ' '  | cut -d ' ' -f 14))			
    
    # ! Gestion de l'aide via l'option -h

    # Usage example.
    usage="usage: tunssh [-h ssh_host] [-u ssh_user] [-p ssh_port] [-rth remote_tunnel_host] [-rtp remote_tunnel_port] [-ltp local_tunnel_port] [-v] [-l|--list] [-k] [-ka|--kill-all]"
    
    # Arguments.
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
        # Remote tunnel host.
        -rth)
            shift
            remote_tunnel_host=$1
        ;;
        # Remote tunnel port.
        -rtp)
            shift
            remote_tunnel_port=$1
        ;;
        # Local tunnel port.
        -ltp)
            shift
            local_tunnel_port=$1
        ;;
        # List all ssh tunnel.
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
            pkill ssh -fN -L
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
        
        # Next arg.
        shift
        
    done


    # ! Manage default values.
    
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
        echo -n "Entrer le numéro du port SSH de la machine distante [22] : " 
        read ssh_port
        if [[ ! $ssh_port ]]
        then
            ssh_port='22'
        fi
    fi
    
    # Remote tunnel host :
    if [[ ! $remote_tunnel_host ]]
    then
        echo -n "Entrer l'IP ou le nom de domaine local de la machine sur le réseau distant depuis laquelle vous souhaitez ouvir un tunnel [localhost] : " 
        read remote_tunnel_host
        if [[ ! $remote_tunnel_host ]]
        then
            remote_tunnel_host='localhost'
        fi
    fi
    
    # Remote tunnel port :
    if [[ ! $remote_tunnel_port ]]
    then
        echo -n "Entrer le numéro de port distant que vous souhaitez transférer en local [80] : " 
        read remote_tunnel_port
        if [[ ! $remote_tunnel_port ]]
        then
            remote_tunnel_port='80'
        fi
    fi
    
    # Local tunnel port :
    if [[ ! $local_tunnel_port ]]
    then
        echo -n "Entrer le numéro de port local sur lequel vous souhaitez transférer le port distant [8080] : " 
        read local_tunnel_port
        if [[ ! $local_tunnel_port ]]
        then
            local_tunnel_port='8080'
        fi
    fi
    
    # ! Show values.
    
    # Check verbose mode.
    if [[ $verbose_mode == 1 ]]
    then
        # Show values.
        echo "SSH host = $ssh_host"
        echo "SSH user = $ssh_user"
        echo "SSH port = $ssh_port"
        echo "Tunnel remote host = $remote_tunnel_host"
        echo "Tunnel remote port = $remote_tunnel_port"
        echo "Tunnel local port = $local_tunnel_port"
    fi
    
    # ! Controls
    
    # Si tunnel déjà ouvert.
    #tunnel_value="$local_tunnel_port:$remote_tunnel_host:$remote_tunnel_port"
    #if [[ " ${tunnel_list[@]} " =~ " ${$tunnel_value} " ]]
    #then
    #  echo "Un tunnel est déjà ouvert : [$tunnel_value]"
    #  return -1
    #fi
    
    # ! Tunnel SSH
    
    # Create SSH tunneling command (-fN = -f + -N)
    # -f : Go in background mode after connexion.
    # -N : No command to lauch in background mode.
    sshtun="ssh -fN -L $local_tunnel_port:$remote_tunnel_host:$remote_tunnel_port $ssh_user@$ssh_host -p $ssh_port"
    
    # Check verbose mode.
    if [[ $verbose_mode == 1 ]]
    then 
        # Show command.
        echo "Lancement de la commande SSH :"
        echo $sshtun
    fi
    
    # Initiate SSH tunneling in background mode.
    eval $sshtun
    echo "Tunnel ouvert : $ssh_host:$remote_tunnel_host:$remote_tunnel_port => localhost:$local_tunnel_port"
    
    # Check verbose mode.
    if [[ $verbose_mode == 1 ]]
    then 
        # Show connection info.
        echo "Vous pouvez dès à présent vous connecter au service proposer par se port en utilisant votre logiciel favoris via l'adresse localhost:$local_tunnel_port"
        echo "Par exemple si le port propose un service HTTP vous pouvez vous accéder au service en utilisant votre navigateur préféré et en vous connectant sur http://localhost:$local_tunnel_port"
    fi
    
    # End.
    return -1
    
}