##!/bin/bash
#PBS -N GATK_Family_8Y2781
#PBS -l nodes=node02:ppn=30
#PBS -l mem=60G
#PBS -q default
#PBS -o /home/yyy/Data/Changsha_WES/CaseAnalysis/8Y2781/PBSlog/PBS_log
#PBS -e /home/yyy/Data/Changsha_WES/CaseAnalysis/8Y2781/PBSlog/PBS_log

#assign the variables
nt=30
familyID=("N8297" "N8298" "N8299" "N8300" "N8306" "N8410")
pipsoft="GATK"
chr=("chr1" "chr2" "chr3" "chr4" "chr5" "chr6" "chr7" "chr8" "chr9" "chr10" "chr11" "chr12" "chr13" "chr14" "chr15" "chr16" "chr17" "chr18" "chr19" "chr20" "chr21" "chr22" "chrX" "chrY" "chrM")

#assign the file catalog
casedir="/home/yyy/Data/Changsha/WG_analysis/20201103/Cases"

#common resource and software
resources="/public1/data/resources"
fasta=${resources}"/ref_genome/hg19/ucsc.hg19.fasta"
hg19_ref="/home/yyy/resources/hg19/ref_variants"
soft="/sdb1/tools/wgss"
bwa=${soft}"/bwa/bwa"
GATK=${soft}"/GATK-4.1.4.0/gatk"
picard=${soft}"/picard/picard.jar"
samtools=${soft}"/samtools/bin/samtools"


# 遍历case进行分染色体的合并
for fam in ${familyID[@]}
do {
  #assign the work catalog
  tmpdir=$casedir/$fam/$pipsoft
  result=$tmpdir/result

  if [ ! -d $result ]; then
	mkdir -p $result
  fi

  # Use GenomicsDBImport to combine the g.vcf for multi-samples（-V gendb://$result）
  # One or more genomic intervals are required as input
  #-L chr1 一次只能处理一条染⾊体，或⼀个interval，可以用脚本分别操作后,再⽤CombineVariants合并
  echo "GenomicsDBImport start for combining the gvcfs in chromosome!"
  for ch in ${chr[@]}
  do {
    tmp=$result/$ch

    $GATK --java-options "-Xmx60G -Xms60G" GenomicsDBImport \
    -L $ch \
    --genomicsdb-workspace-path $tmp \
    `cat $tmpdir/vcflist.txt`

    }&
  done
  wait
  echo gatk-GenomicsDBImport `date`
  echo "GenomicsDBImport finished................................!"

  # joint genotyping using g.vcf
  # -V参数指定的是GenomicsDBImport输出目录的路径
  #-L #可选
  echo "GenotypeGVCFs start for generating the final vcf!"
  for ch in ${chr[@]}
  do {
    if [ ! -d $result/vcfchr ]; then
      mkdir -p $result/vcfchr
    fi

    $GATK --java-options "-Xmx60G -Djava.io.tmpdir=/public1/tmp/yyy/changsha" GenotypeGVCFs \
    -R $fasta \
    -O ${result}/vcfchr/${familyID}_${pipsoft}_raw_${ch}.vcf \
    -D $hg19_ref/dbsnp_138.hg19.vcf \
    -V gendb://$result/$ch

    }&
  done
  wait
  echo gatk-GenotypeGVCFs `date`
  echo "GenotypeGVCFs finished.........................!"

  # merge all the vcf for chr into one vcf file
  $GATK MergeVcfs $(for i in {1..22} X Y M;do echo "-I ${result}/vcfchr/Diabetes_GATK_raw_chr${i}.vcf";done) -O ${result}/Diabetes_GATK_raw_merge.vcf
}
