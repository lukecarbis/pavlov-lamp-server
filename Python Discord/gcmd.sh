# Peter Wilson
# This script needs to have gcloud installed in order for it to send comands to GCP
# https://cloud.google.com/sdk/docs/install
# Get arguments 
# Verson 1
while getopts m:p:s:u: flag
do
    case "${flag}" in
        m) vm_name=${OPTARG};; # Getting the VM name in GCP
        p) vm_power=${OPTARG};; # Starting or stopping VM in GCP
        s) vm_status=${OPTARG};; # Checking the status of the VM
        u) bot_update=${OPTARG};; # Download updates from gcloud
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
        echo "I was able to $vm_power $vm_name successfully... Not that anyone cares." 
    else
        echo "hmmm! Sorry I wasn't able to $vm_power $vm_name. This will all end in tears I just know it." 
    fi
fi

# Check all VM Stuts
if [ -n "$vm_status" ];
then
    # output the list to a temp file
    gcloud compute instances list > ./tmp_status
fi
echo $bot_update
# Download files from gcloud
if [ -n "$bot_update" ];
then
    # Download the files needed.
    gsutil cp gs://lamp-bot-prod/* ./updater
    # listed the downloaded files
    ls ./updater > ./tmp_update
fi