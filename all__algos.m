close all
clear all
% the directory and files will be saved based on the image name
% Thus we just change the sequence / image name and the whole analysis is
% done for that particular sequence
imageName = 'caltrain';
mbSize = 8;
p = 7;
%for i = 0:30

   
    imgIFile =  sprintf('1.png');
    imgPFile =  sprintf('4.png');

    imgI = double(imread(imgIFile));
    imgP = double(imread(imgPFile));
    imgI = imgI(:,1:352);
    imgP = imgP(:,1:352);

    % Adaptive Rood Patern Search
    [motionVect, computations] = motionEstARPS(imgP,imgI,mbSize,p);
    imgComp = motionComp(imgI, motionVect, mbSize);
    ARPSpsnr(1) = imgPSNR(imgP, imgComp, 255); 
    ARPScomputations(1) = computations;
%end
%save dsplots2 DSpsnr DScomputations ESpsnr EScomputations TSSpsnr ...
%      TSScomputations SS4psnr SS4computations NTSSpsnr NTSScomputations ...
%       SESTSSpsnr SESTSScomputations ARPSpsnr ARPScomputations

save RPSpsnr ARPScomputations
