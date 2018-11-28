#!//bin/ksh

SYSTEM=on.tmstv.com
USER=onsample
PASSWORD=638kd307
DIRECTORY=/
BASEDIRECTORY=/home/zappware/TVAnywhere
WORKINGLOCALDIRECTORY=$BASEDIRECTORY/working
ZAPPWARETOlOAD=$WORKINGLOCALDIRECTORY/graceNoteInputFiles
TMPTOLOAD=$WORKINGLOCALDIRECTORY/graceNoteInputFiles
TODO=$WORKINGLOCALDIRECTORY/todo.lst
#TODOA=/home/zappware/tmp/Aneishatodo.lst
tmpfile=$WORKINGLOCALDIRECTORY/ftpdir
#PATHTOREPLACEICON=/home/zappware/updatedTmpToLoad/*.xml

#empty directory before processing
#find /home/zappware/updatedTmpToLoad -name "*.xml" -type f -delete
#find $TMPTOLOAD -name "*.xml" -type f -delete


exec 5>&1 >$tmpfile 4>&1  
ftp -nv >&4 2>&4|&
print -p open $SYSTEM
print -p user $USER $PASSWORD
print -p cd $DIRECTORY
print -p nlist
print -p bye
wait
exec >&5 2>&1 < $tmpfile

# only store xml files
cat $tmpfile | grep on_car_samp_tv_[ps] > $WORKINGLOCALDIRECTORY/filesToGet
#rm /home/zappware/tmp/updatedfilesToGet
#grep "$(date +%Y%m%d)" /home/zappware/tmp/filesToGet  >>/home/zappware/tmp/updatedfilesToGet

#grep "$(date --date="3 days ago" +%Y%m%d)"  /home/zappware/tmp/filesToGet  >>/home/zappware/tmp/updatedfilesToGet

>$TODO
echo >>$TODO user $USER $PASSWORD
echo >>$TODO cd $DIRECTORY
echo >>$TODO lcd $TMPTOLOAD
echo >>$TODO binary
while read N
do
   echo >>$TODO get $N
done < $WORKINGLOCALDIRECTORY/filesToGet
 
echo >>$TODO quit


ftp -nv $SYSTEM <$TODO

#copy all files in tmp to load to the updatedTmpToLoad
#cp /home/zappware/tmpToLoad/*.xml /home/zappware/updatedTmpToLoad



#/bin/bash /home/zappware/scripts/updated_production_gracenote_to_zappware_Pictures.sh
cd $ZAPPWARETOlOAD
rm *.xml
gunzip *.gz
mv on_car_samp_tv_sources_v22_2*.xml on_car_samp_tv_sources_v22_current.xml
mv on_car_samp_tv_schedules_v22_2*.xml on_car_samp_tv_schedules_v22_current.xml
mv on_car_samp_tv_programs_v22_2*.xml on_car_samp_tv_programs_v22_current.xml

#start BaseX Server
$BASEDIRECTORY/basex/bin/basexserver -z
$BASEDIRECTORY/basex/bin/basex -c$BASEDIRECTORY/basexCreateDBs.txt

cd $WORKINGLOCALDIRECTORY
$BASEDIRECTORY/python3.6Env/bin/python $BASEDIRECTORY/ZappwareEPGConvert/epgconvert/epg_convert.py


#Stop Basex Server if desired
#/home/tdeane/TVAnywhere/basex/bin/basexserverstop

