import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

## L2 norm
def distance(image1, image2):
    difference = image1 - image2
    return np.sum(difference**2)

class KMeans(object):
    # K is the K in KMeans
    # useKMeansPP is a boolean. If True, initialize using KMeans++
    def __init__(self, K, useKMeansPP):
        self.K = K
        self.useKMeansPP = useKMeansPP

    # X is a (N x 28 x 28) array where 28x28 is the dimensions of each of the N images.
    def fit(self, X, show_initial=False):
        ### Create an empty array of K cluster centers that will be initialized and updated. 
        cluster_centers = np.zeros((self.K, X.shape[1], X.shape[2]))

        ### Create arrays to store the cluster identities of each image.
        N = X.shape[0] # number of images
        cluster_ids = np.zeros(N)
        cluster_ids_old = np.zeros(N) # To hold last iteration's clusters to compare for convergence.

        if self.useKMeansPP==False:
            # 1) Define random initial cluster centers using Forgy's method:

            ### Sample indices for the points that will be used as initial cluster centers:
            idxs = np.random.choice(X.shape[0], self.K, replace=False)

            ### Assign the sampled points to be the initial cluster centers. 
            cluster_centers[range(self.K)] = X[idxs]

        else: # K-means ++
            ### Pick the first cluster center randomly.
            cluster_centers[0] = X[np.random.randint(N)]

            ### Array of probabilities of selecting each point to be the next cluster center.
            prob = np.zeros(N)

            for i in range(1,self.K):
                # For each of the remaining cluster centers, calculate distances from each cluster
                #   center that has been defined to each data point, and assign the minimum of these
                #   distances as the probability of selecting that point to be the next cluster center.  
                for k in range(N):
                    prob[k] = np.min([distance(X[k], cluster_centers[j]) for j in range(0,i+1)])
                # Normalize probabilities.  
                prob = prob/sum(prob)
                # Select index of the next cluster
                index_of_next_cluster_center = np.random.choice(range(N),size=1,p=prob)
                cluster_centers[i] = X[index_of_next_cluster_center]

        if show_initial==True: # Show initial cluster means
            initials = np.zeros((X.shape[1], self.K*X.shape[2]))
            for i in range(self.K):
                initials[:,i*X.shape[2]:(i+1)*X.shape[2]] = cluster_centers[i]
            plt.figure()
            plt.imshow(-initials, cmap='Greys_r')
            plt.savefig('img12.png')
            plt.show()

        # 2) Start iteratively assigning all the images to their closest cluster center

        counter = 0

        # Array used to store distances used to calculate objective function.  
        objectives = np.zeros(N)
        # List of objective function values at each iteration
        objective = []

        while True:#not converged:
            # Assign every image to its closest cluster center
            for i in range(N):
                # Calculate norm to every cluster center and store to calculate objective function value
                dists = [distance(X[i], cluster_centers[j]) for j in range(self.K)]
                objectives[i] = np.min(dists)

                # Assign the image to the closest cluster center.
                cluster_id = np.argmin(dists)
                cluster_ids[i] = cluster_id

            objective.append(np.sum(objectives))
            # Verify that objective function only increases:
            if objective[counter] > objective[counter-1]:
                print "Objective function increased!"
            
            # After each pass through all the images, update the cluster centers to the mean of each.
            cluster_centers = [np.mean(X[cluster_ids==i], axis=0) for i in range(self.K)]

            # After each pass through all the images, check for convergence.  
            # If the cluster assignments are the same as last iteration, break.   
            if np.array_equal(cluster_ids_old, cluster_ids): 
                break

            # If we haven't converged, keep a copy of this iteration's results for the next one.  
            cluster_ids_old = np.copy(cluster_ids)

            counter += 1
            if counter%1==0:
                print counter

        # Store the images, means, and cluster assignments to use later
        self.X = X
        self.N = len(X)
        self.means = cluster_centers 
        self.clusters = cluster_ids_old

        # Show plot of objective function values over time.  
        plt.figure()
        plt.plot(objective)
        plt.xlabel("Iterations")
        plt.ylabel("Value of Objective Function")
        plt.title("Objective Function Value over Time")
        # plt.savefig("obj.png")
        plt.show()


    # This should return the arrays for K images. Each image should represent the mean of each of the fitted clusters.
    def get_mean_images(self):
        return self.means

    # This should return the arrays for D images from each cluster that are representative of the clusters.
    def get_representative_images(self, D):
        # Here, I define shortest distance to the cluster mean as most representative of the cluster.  

        # Empty array, to fill each row with the representative images for each cluster.  
        rep_images = np.zeros((self.K, D, self.X.shape[1], self.X.shape[2]))

        for i in range(self.K):
            # For each cluster, sort the images by their distance from the cluster mean.  
            
            distances = []              # Distances from mean for each cluster
            idxs = []                   # Indexes of each distance in the distance list
            mask = (self.clusters==i)   # Mask to use only the images in this cluster.  

            for j in range(self.N): 
                if mask[j]==True:   # Consider only the images in this class.
                    # For each image in the cluster, calculate the distance from the cluster mean.  
                    distances.append(distance(self.X[j], self.means[i]))
                    idxs.append(j)

            # Get the indices of the order of the distances for the cluster.     
            order = np.argsort(distances)
            # Take the specified number from the list, and slice out the corresponding indexes from the list
            #   created in the loop.  
            indexes = np.array(idxs)[order[:D]]

            # Use the indexes to call the appropriate images.  
            rep_images[i,:] = self.X[[indexes]]

        return rep_images


    # img_array should be a 2D (square) numpy array.
    # Note, you are welcome to change this function (including its arguments and return values) to suit your needs. 
    # However, we do ask that any images in your writeup be grayscale images, just as in this example.
    def create_image_from_array(self, img_array):
        plt.figure()
        plt.imshow(img_array, cmap='Greys_r')
        plt.savefig('img5.png')
        plt.show()
        return

# This line loads the images.
pics = np.load("images.npy", allow_pickle=False)

K = 10
num_ex = 4

KMeansClassifier = KMeans(K, useKMeansPP=True)
KMeansClassifier.fit(pics, show_initial=False)
cluster_means = KMeansClassifier.get_mean_images()

representative_images = KMeansClassifier.get_representative_images(num_ex)


# Make an empty array to hold the output display.  

# Separator in the output array to distinguish cluster means from representative examples.  
sep_width = 2

# It has a column for the means, a separator
cluster_examples=np.zeros((K * 28, 28 + sep_width + 28*num_ex))

# Fill in the separator as the max pixel value to make a dark vertical bar
cluster_examples[:,28:28+sep_width] = np.max(pics[0])

# Fill in the rows
for i in range(K):
    # Cluster means
    cluster_examples[i*28:(i+1)*28, 0:28] = cluster_means[i]

    for j in range(num_ex):
        # Representative images
        cluster_examples[i*28:(i+1)*28, sep_width+28+j*28:sep_width+28+(j+1)*28]=representative_images[i,j]
        
KMeansClassifier.create_image_from_array(-cluster_examples)