#!/usr/bin/env bash
FILE=Wikipedia_2000_dump.xml
if [ ! -f ${FILE} ]
then
    wget http://mit.spbau.ru/sewiki/images/8/87/${FILE}.gz
    gunzip -d ${FILE}.gz
fi