import {
  Code,
  Collapse,
  Heading,
  Link,
  ListItem,
  OrderedList,
  Table,
  Tbody,
  Td,
  Text,
  Th,
  Thead,
  Tr,
  UnorderedList,
} from "fidesui";
import { ReactNode, useState } from "react";

import Tag from "~/features/common/Tag";

const PROJECT_CREATION_GUIDE_URL =
  "https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project";
const ROLES_GUIDE_URL =
  "https://cloud.google.com/iam/docs/creating-custom-roles#creating_a_custom_role";
const SERVICE_ACCOUNT_GUIDE_URL =
  "https://cloud.google.com/iam/docs/service-accounts-create";

const SAMPLE_JSON = `{
  "type": "service_account",
  "project_id": "project-id-123456",
  "private_key_id": "0123456789abcdef0123456789abcdef01234567",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIyourkey-----\\nEND PRIVATE KEY-----\\n",
  "client_email": "test@project-id-123456.iam.gserviceaccount.com",
  "client_id": "012345678901234567890",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/test%40project-id-123456.iam.gserviceaccount.com"
}`;

const InfoHeading = ({ text }: { text: string }) => (
  <Heading fontSize="sm" mt={4} mb={1}>
    {text}
  </Heading>
);

const InfoText = ({ children }: { children: ReactNode }) => (
  <Text fontSize="14px" mb={4}>
    {children}
  </Text>
);

const InfoLink = ({
  children,
  href,
}: {
  children: ReactNode;
  href: string;
}) => (
  <Link href={href} textDecoration="underline" isExternal>
    {children}
  </Link>
);

const InfoUnorderedList = ({ children }: { children: ReactNode }) => (
  <UnorderedList fontSize="14px" mb={4}>
    {children}
  </UnorderedList>
);

const InfoOrderedList = ({ children }: { children: ReactNode }) => (
  <OrderedList fontSize="14px" mb={4}>
    {children}
  </OrderedList>
);

const BigQueryOverview = () => {
  const [showingMore, setShowingMore] = useState(false);
  return (
    <>
      <InfoHeading text="Overview" />
      <InfoText>
        Continuously monitor BigQuery to detect and track schema-level changes,
        automatically discover and label data categories as well as
        automatically process DSR (privacy requests) and consent enforcement to
        proactively manage data governance risks.
      </InfoText>
      <Collapse in={showingMore}>
        <InfoHeading text="Categories" />
        <InfoUnorderedList>
          <ListItem>Data Warehouse</ListItem>
          <ListItem>Storage system</ListItem>
          <ListItem>Cloud provider</ListItem>
          <ListItem>Data detection</ListItem>
          <ListItem>Data discovery</ListItem>
          <ListItem>DSR automation</ListItem>
          <ListItem>Consent orchestration</ListItem>
        </InfoUnorderedList>
        <InfoHeading text="Permissions" />
        <InfoText>
          For detection and discovery, Fides requires a read-only BigQuery
          service account with limited permissions. If you intend to automate
          governance for DSR or Consent, Fides requires a read-and-write
          BigQuery service account to any project you would like Fides to
          govern.
        </InfoText>
        <InfoText>
          A BigQuery administrator can create the necessary role for Fides using
          BigQuery&apos;s roles guide and assign this to a service account using
          BigQuery&apos;s service account guide.
        </InfoText>
        <InfoText>
          The permissions allow Fides to read the schema of, and data stored in
          projects, datasets and tables as well write restricted updates based
          on your policy configurations to tables you specify as part of DSR and
          Consent orchestration.
        </InfoText>
        <InfoHeading text="Permissions list" />
        <InfoUnorderedList>
          <ListItem>bigquery.jobs.create</ListItem>
          <ListItem>bigquery.jobs.list</ListItem>
          <ListItem>bigquery.routines.get</ListItem>
          <ListItem>bigquery.routines.list</ListItem>
          <ListItem>bigquery.datasets.get</ListItem>
          <ListItem>bigquery.tables.get</ListItem>
          <ListItem>bigquery.tables.getData</ListItem>
          <ListItem>bigquery.tables.list</ListItem>
          <ListItem>bigquery.tables.updateData</ListItem>
          <ListItem>bigquery.projects.get</ListItem>
        </InfoUnorderedList>
      </Collapse>
      <Text
        fontSize="14px"
        cursor="pointer"
        textDecoration="underline"
        onClick={() => setShowingMore(!showingMore)}
      >
        {showingMore ? "Show less" : "Show more"}
      </Text>
    </>
  );
};

export const BigQueryInstructions = () => {
  const [showingMore, setShowingMore] = useState(false);

  return (
    <>
      <InfoHeading text="Configuring a Fides -> BigQuery Integration" />
      <InfoHeading text="Step 1: Create a Fides project" />
      <InfoText>
        Create a Fides Project using{" "}
        <InfoLink href={PROJECT_CREATION_GUIDE_URL}>
          BigQuery&apos;s project creation guide
        </InfoLink>
        .
      </InfoText>
      <InfoHeading text="Step 2: Create a Fides role in GCP" />
      <InfoOrderedList>
        <ListItem>
          Create a custom role for Fides using BigQuery&apos;s{" "}
          <InfoLink href={ROLES_GUIDE_URL}>roles guide</InfoLink>.
        </ListItem>
        <ListItem>
          Follow the sections below to grant permissions to this role for the
          Fides project and any project you would like Fides to manage.
        </ListItem>
      </InfoOrderedList>
      <Collapse in={showingMore}>
        <InfoHeading text="Step 3: Assign permissions to the Fides project" />
        <InfoText>
          Assign the following permissions to the Fides Project that will be
          used by your Fides service account to run queries:
        </InfoText>
        <Table fontSize="14px">
          <Thead>
            <Tr>
              <Th>Permission</Th>
              <Th>Description</Th>
            </Tr>
          </Thead>
          <Tbody>
            <Tr>
              <Td>
                <Tag>bigquery.jobs.create</Tag>
              </Td>
              <Td>
                Run jobs (e.g. queries) within the project. This is only needed
                for the Fides Project where the Fides service account is
                located.
              </Td>
            </Tr>
            <Tr>
              <Td>
                <Tag>bigquery.jobs.list</Tag>
              </Td>
              <Td>
                Manage the queries that the service account performs. This is
                only needed for the Fides Project where the Fides service
                account is located.
              </Td>
            </Tr>
            <Tr>
              <Td>
                <Tag>bigquery.routines.get</Tag>
              </Td>
              <Td>
                Allow the service account to retrieve custom routines (e.g.
                queries) on associated datasets and tables.
              </Td>
            </Tr>
            <Tr>
              <Td>
                <Tag>bigquery.routines.list</Tag>
              </Td>
              <Td>
                Allow the service account to manage the custom routines (e.g.
                queries) that run on associated datasets and tables.
              </Td>
            </Tr>
          </Tbody>
        </Table>
        <InfoHeading text="Step 4: Assign permissions to any project you’d like Fides to monitor" />
        <InfoText>
          Grant the following permissions to the Fides service account in every
          project where you would like Fides detection and discovery monitoring.
        </InfoText>
        <Table fontSize="14px">
          <Thead>
            <Tr>
              <Th>Permission</Th>
              <Th>Description</Th>
            </Tr>
          </Thead>
          <Tbody>
            <Tr>
              <Td>
                <Tag>bigquery.datasets.get</Tag>
              </Td>
              <Td>
                Retrieve metadata and list tables for the specified project.
              </Td>
            </Tr>
            <Tr>
              <Td>
                <Tag>bigquery.tables.get</Tag>
              </Td>
              <Td>Retrieve metadata for the specified table.</Td>
            </Tr>
            <Tr>
              <Td>
                <Tag>bigquery.tables.getData</Tag>
              </Td>
              <Td>Read data in the specified table.</Td>
            </Tr>
            <Tr>
              <Td>
                <Tag>bigquery.tables.list</Tag>
              </Td>
              <Td>List all tables in the specified dataset.</Td>
            </Tr>
            <Tr>
              <Td>
                <Tag>bigquery.projects.get</Tag>
              </Td>
              <Td>Retrieve metadata for the specified project.</Td>
            </Tr>
          </Tbody>
        </Table>
        <InfoHeading text="Step 5: Create a Fides service account in the Fides Project" />
        <InfoOrderedList>
          <ListItem>
            Create a service account for Fides using BigQuery&apos;s{" "}
            <InfoLink href={SERVICE_ACCOUNT_GUIDE_URL}>
              service account guide
            </InfoLink>
            .
          </ListItem>
          <ListItem>
            Assign the previously created role to this service account.
          </ListItem>
          <ListItem>
            Download the service account JSON keyfile.{" "}
            <strong>
              Note: this is sensitive information that should not be shared.
            </strong>{" "}
            An example of this is below:
          </ListItem>
        </InfoOrderedList>
        <Code display="block" whiteSpace="pre" p={4} mb={4} overflowX="scroll">
          {SAMPLE_JSON}
        </Code>
        <InfoHeading text="Step 6: Use the JSON key to authenticate your integration" />
        <InfoText>
          Provide the JSON key to your Fides instance to securely connect Fides.
        </InfoText>
      </Collapse>
      <Text
        fontSize="14px"
        cursor="pointer"
        textDecoration="underline"
        onClick={() => setShowingMore(!showingMore)}
      >
        {showingMore ? "Show less" : "Show more"}
      </Text>
    </>
  );
};

export default BigQueryOverview;
