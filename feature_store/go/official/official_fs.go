package main

import (
	"context"
	"fmt"

	"google.golang.org/api/option"

	aiplatform "cloud.google.com/go/aiplatform/apiv1"
	aiplatformpb "google.golang.org/genproto/googleapis/cloud/aiplatform/v1"
)

func main() {
	ctx := context.Background()
	c, err := aiplatform.NewFeaturestoreOnlineServingClient(ctx,
		option.WithEndpoint("asia-southeast1-aiplatform.googleapis.com:443"))
	if err != nil {
		// TODO: Handle error.
		fmt.Println("error creating client")
		fmt.Println(err)
	}
	defer c.Close()

	req := &aiplatformpb.ReadFeatureValuesRequest{
		// TODO: Fill request struct fields.
		// See https://pkg.go.dev/google.golang.org/genproto/googleapis/cloud/aiplatform/v1#ReadFeatureValuesRequest.
		EntityType: "projects/832137092875/locations/asia-southeast1/featurestores/marketing_featurestore/entityTypes/users",
		EntityId:   "UID2733",
		FeatureSelector: &aiplatformpb.FeatureSelector{
			IdMatcher: &aiplatformpb.IdMatcher{
				Ids: []string{"channel", "history"},
			},
		},
	}
	resp, err := c.ReadFeatureValues(ctx, req)
	if err != nil {
		// TODO: Handle error.
		fmt.Println("error calling ReadFeatureValues")
		fmt.Println(err)
	}
	// TODO: Use resp.
	fmt.Println(resp)
}
