# Peter Wilson
# This script needs to have gcloud installed in order for it to send comands to GCP
# https://cloud.google.com/sdk/docs/install
# Get arguments 
while getopts m:p:s:c: flag
do
    case "${flag}" in
        m) vm_name=${OPTARG};; # Getting the VM name in GCP
        p) vm_power=${OPTARG};; # Starting or stopping VM in GCP
        s) vm_status=${OPTARG};; # Checking the status of the VM
        #c) vm_cost=${OPTARG};; # Getting the cost of GCP
    esac
done

# For starting or stopping the VM
# Check is -p was arguments is not empty
if [ -n "$vm_power" ];
then
    # Run the gcloud cmd
    gcloud compute instances $vm_power $vm_name > ./tmp

    # Get the results and echo back.
    if [ "$?" -eq "0" ]
    then
        echo "I was able to $vm_power $vm_name successfully." 
    else
        echo "hmmm! Sorry I wasn't able to $vm_power $vm_name." 
    fi
fi

# Check all VM Stuts
if [ -n "$vm_status" ];
then
    # output the list to a temp file
    gcloud compute instances list > ./tmp_status
fi