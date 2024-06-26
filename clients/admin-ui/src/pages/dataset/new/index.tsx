import { Box, Button, Heading, Stack } from "fidesui";
import type { NextPage } from "next";
import { useState } from "react";

import { useFeatures } from "~/features/common/features";
import Layout from "~/features/common/Layout";
import BackButton from "~/features/common/nav/v2/BackButton";
import { DATASET_ROUTE } from "~/features/common/nav/v2/routes";
import QuestionTooltip from "~/features/common/QuestionTooltip";
import DatabaseConnectForm from "~/features/dataset/DatabaseConnectForm";
import DatasetYamlForm from "~/features/dataset/DatasetYamlForm";

const NewDataset: NextPage = () => {
  const features = useFeatures();
  const [generateMethod, setGenerateMethod] = useState<
    "yaml" | "database" | "manual" | null
  >(null);
  return (
    <Layout title="Create New Dataset">
      <BackButton backPath={DATASET_ROUTE} />
      <Heading mb={8} fontSize="2xl" fontWeight="semibold">
        Create New Dataset
      </Heading>
      <Stack spacing={8}>
        <Box>
          <Button
            size="sm"
            mr={2}
            variant="outline"
            onClick={() => setGenerateMethod("yaml")}
            isActive={generateMethod === "yaml"}
            data-testid="upload-yaml-btn"
          >
            Upload a Dataset YAML
          </Button>
          <Button
            size="sm"
            mr={2}
            variant="outline"
            onClick={() => setGenerateMethod("database")}
            isActive={generateMethod === "database"}
            isDisabled={features.flags.dataDiscoveryAndDetection}
            data-testid="connect-db-btn"
          >
            Connect to a database
          </Button>
          {features.flags.dataDiscoveryAndDetection ? (
            <QuestionTooltip label="Creating a dataset via a database connection is disabled when the 'detection & discovery' beta feature is enabled" />
          ) : null}
        </Box>
        {generateMethod === "database" && (
          <Box w={{ base: "100%", lg: "50%" }}>
            <DatabaseConnectForm />
          </Box>
        )}
        {generateMethod === "yaml" && (
          <Box w={{ base: "100%" }}>
            <DatasetYamlForm />
          </Box>
        )}
      </Stack>
    </Layout>
  );
};

export default NewDataset;
