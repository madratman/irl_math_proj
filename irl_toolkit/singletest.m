clear all
clc

% Convenience script for running a single test.
addpaths;

%% Added to bring in features from our demonstrations
% pathName1='../data/';
% pathName2='/features/dist_onehot/a_star_traj_';
% pathName3='.txt';
% pathName4='/all_dist_onehot.txt';
pathName1='../data/';
pathName2='/features/final/a_star_traj_';
pathName3='.txt';
pathName4='/all_final.txt';
pathName5='/features/final/a_star_traj_';
n=100;

features=cell(0);
features_total=cell(0);
lastIndex=1;
for i=1:10
    scenarioNumber=num2str(i-1,'%02d');
    totalName_totalFeat=strcat(pathName1,scenarioNumber,pathName4);
    features_total{i}=textread(totalName_totalFeat);
    
%     c1=sqrt(features_total{i}(:,6));
%     c2=sqrt(features_total{i}(:,10));
%     c3=sqrt(features_total{i}(:,14));
%     c4=sqrt(features_total{i}(:,18));
%     c5=sqrt(features_total{i}(:,22));
%     c6=ones(size(features_total{i}(:,1)));
%     features_total{i}=[features_total{i}(:,1:6),c1,features_total{i}(:,7:10),c2,features_total{i}(:,11:14),c3,features_total{i}(:,15:18),c4,features_total{i}(:,19:22),c5,c6];
%     
    c6=ones(size(features_total{i}(:,1)));
    features_total{i}=[features_total{i}(:,1:end),c6];
    
    for j=1:35
        trialNumber=num2str(j-1,'%02d');
        totalName=strcat(pathName1,scenarioNumber,pathName2,trialNumber,pathName3);
        features{i}{j}=textread(totalName);
        
%         % 1/d
%         d1=10./(1./(features{i}{j}(:,6))+9);
%         d2=10./(1./(features{i}{j}(:,10))+9);
%         d3=10./(1./(features{i}{j}(:,14))+9);
%         d4=10./(1./(features{i}{j}(:,18))+9);
%         d5=10./(1./(features{i}{j}(:,22))+9);
%         
%         %1/d^2
%         c1=1000./((1./(features{i}{j}(:,6))-1).^2+1000);
%         c2=1000./((1./(features{i}{j}(:,10))-1).^2+1000);
%         c3=1000./((1./(features{i}{j}(:,14))-1).^2+1000);
%         c4=1000./((1./(features{i}{j}(:,18))-1).^2+1000);
%         c5=1000./((1./(features{i}{j}(:,22))-1).^2+1000);
%         
 
%         c1=(features{i}{j}(:,6)).^2;
%         c2=(features{i}{j}(:,10)).^2;
%         c3=(features{i}{j}(:,14)).^2;
%         c4=(features{i}{j}(:,18)).^2;
%         c5=(features{i}{j}(:,22)).^2;

        c6=ones(size(features{i}{j}(:,1)));
%         
%         features{i}{j}=[features{i}{j}(:,1:5),d1,c1,features{i}{j}(:,7:9),d2,c2,features{i}{j}(:,11:13),d3,c3,features{i}{j}(:,15:17),d4,c4,features{i}{j}(:,19:21),d5,c5,c6];

        features{i}{j}=[features{i}{j}(:,1:end),c6];
 
    end
end

example_samples_total=cell(0);
for i=1:10
    for j=1:35
        for k=1:size(features{i}{j},1)
            x=features{i}{j}(k,1);
            y=features{i}{j}(k,2);
            s = y*n+x+1;
            if k<size(features{i}{j},1)
                xNext=features{i}{j}(k+1,1);
                yNext=features{i}{j}(k+1,2);
                action=defineAction(x,y,xNext,yNext);
            else
                action=randi([1,9],1);
            end
            example_samples_total{i}{j,k}=[s;action];
        end
    end
end

%%

% get all features from all the map
w_vec=cell(0);
featuresMap=cell(0);
costMap=cell(0);

for i=1:10
    i
    features_totalTrial=-features_total{i}(:,3:(end-1)); % don't include bias here, he adds later in mmprun
    example_samples_Trial=example_samples_total{i};
    
    [w_vec{i},featuresMap{i},costMap{i}] = runtest('mmp',struct(),'linearmdp',...
        'objectworld',struct('n',100,'determinism',1,'seed',1,'continuous',0),...
        struct('training_sample_lengths',8,'training_samples',35,'verbosity',2),example_samples_Trial,features_totalTrial);
end



% figure
% contour(costMap)
% figure
% imagesc(costMap)

%% Visualize solution. -- REMOVED FOR NOW
% printresult(test_result);
% visualize(test_result);


