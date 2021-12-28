function [C, sigma] = dataset3Params(X, y, Xval, yval)
%DATASET3PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = DATASET3PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.
C = 1;
sigma = 0.3;

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
%

%create vector of parameters to try out
C_vec = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30];%linspace(.1, 1, 10);
sigma_vec = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30]; %linspace(.1, 1, 10);

%cartesian product of the above parameters
[C_pts, sigma_pts] = meshgrid(C_vec, sigma_vec);
C_sigma_prod = [C_pts(:), sigma_pts(:)];

%loop through pair of values to see which gives the lowest values of error
error = zeros(length(C_vec),1);

min_error = intmax;

for i=1:length(C_sigma_prod)
    C_i = C_sigma_prod(i, 1);
    sigma_i = C_sigma_prod(i, 2);
    
    model = svmTrain(X, y, C_i, @(x1, x2)gaussianKernel(x1, x2, sigma_i));
    predictions = svmPredict(model, Xval);

    error = mean(double(predictions ~= yval));
    
    if(error < min_error)
        C = C_i;
        sigma = sigma_i;
        min_error = error;
    end
    
end

%min_index = find(error==min(error));
%C = C_sigma_prod(min_index, 1);
%sigma = C_sigma_prod(min_index, 2); 
% =========================================================================

end
