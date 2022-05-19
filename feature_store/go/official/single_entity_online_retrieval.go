package main

import (
	"context"
	"fmt"

	"google.golang.org/api/option"

	aiplatform "cloud.google.com/go/aiplatform/apiv1"
	aiplatformpb "google.golang.org/genproto/googleapis/cloud/aiplatform/v1"
)

func main() {

	region := "asia-southeast1"
	url := fmt.Sprintf("%s-aiplatform.googleapis.com:443", region)

	ctx := context.Background()
	c, err := aiplatform.NewFeaturestoreOnlineServingClient(ctx,
		option.WithEndpoint(url))
	if err != nil {
		fmt.Println("error creating client")
		fmt.Println(err)
	}
	defer c.Close()

	projectId := "mitochondrion-project-344303"
	fsName := "marketing_featurestore"
	entityTypes := "users"
	entityType := fmt.Sprintf("projects/%s/locations/%s/featurestores/%s/entityTypes/%s", projectId, region, fsName, entityTypes)

	entityId := "UID2733"
	featureNames := []string{"channel", "history"}

	req := &aiplatformpb.ReadFeatureValuesRequest{
		EntityType: entityType,
		EntityId:   entityId,
		FeatureSelector: &aiplatformpb.FeatureSelector{
			IdMatcher: &aiplatformpb.IdMatcher{
				Ids: featureNames,
			},
		},
	}
	resp, err := c.ReadFeatureValues(ctx, req)
	if err != nil {
		fmt.Println("error calling ReadFeatureValues")
		fmt.Println(err)
	}
	fmt.Println(resp)
}
