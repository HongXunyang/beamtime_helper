%-----------------------------------------------------------------------------
% Leonardo Martinelli
%-----------------------------------------------------------

function [allScans, miller]=specRead_leo(filename,scans)

%filename is the name of the file, WITH THE PATH
%scans is a character vector with the numbers. You can generate it with
%e.g. num2str([#1 #2 #3...]);

%allScans is a matrix with:
%[energy1 rixs1 energy2 rixs2 ...]

%miller contains the miller indices

[data_all,colname_all,motval_all,motname_all,date] = myspecread_multiple_2020(filename,scans);

allScans = zeros(length(data_all{1}(:,1)), length(data_all)*2);
for ii=1:length(data_all)
    %for each scan 
    
    if sum(strcmp(colname_all{ii}, 'Energy'))>0.1
        indEnergy = find(strcmp(colname_all{ii}, 'Energy'));
    elseif sum(strcmp(colname_all{ii}, 'Energy (eV)'))>0.1
        indEnergy = find(strcmp(colname_all{ii}, 'Energy (eV)'));
    else
        indEnergy = find(strcmp(colname_all{ii}, ' Pixel'));
    end
    indSPC = find(strcmp(colname_all{ii}, 'SPC'));
    indMirror = find(strcmp(colname_all{ii}, 'Mirror current / 1e6'));
    
%     indH= find(strcmp(motname_all{ii}(1,1:124), 'H'));
%     indK = find(strcmp(motname_all{ii}(1,1:124), 'K'));
%     indL = find(strcmp(motname_all{ii}(1,1:124), 'L'));

    indH = 122;
    indK = 123;
    indL = 124;
    
    energy = data_all{ii}(:,indEnergy);
    SPC = data_all{ii}(:,indSPC);
    normal = data_all{ii}(:,indMirror);
    
    H(ii,1) = motval_all{ii}(indH);
    K(ii,1) = motval_all{ii}(indK);
    L(ii,1) = motval_all{ii}(indL);
    
    miller = [H,K,L];
    if length(energy)>=size(allScans,1)
%         allScans(:,ii*2-1:ii*2) = [-flip(energy(1:size(allScans,1))), flip(SPC(1:size(allScans,1)))./normal(1:size(allScans,1))];
        allScans(:,ii*2-1:ii*2) = [energy(1:size(allScans,1)), SPC(1:size(allScans,1))./normal(1:size(allScans,1))];
        
    elseif length(energy)<size(allScans,1)
        allScans = allScans(1:length(energy),:);
%         allScans(:,ii*2-1:ii*2) = [-flip(energy), flip(SPC)./normal];
        allScans(:,ii*2-1:ii*2) = [energy, SPC./normal];
        
    end
    
end

end
